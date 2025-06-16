from datetime import datetime
from typing import Optional

import pandas as pd
import polars as pl
from common.parcer.abstract import PolarsParcer
from common.validation_errors import PresentationDataForError
from django.core.files.uploadedfile import InMemoryUploadedFile
from gas_service.models import GSIndicator, GSInstallation, GSTypePlan
from gas_service.parsers.config import (
    DataFrameData,
    ProductionProductColumns,
    ProductionProductColumnsLoadDB,
    ProductionProductExcelConfig,
    ValidationData,
)
from gas_service.queries import HandbookLoader
from gas_service.validation.production_product import ProductionProductValidator


class ProductionProductParcer(PolarsParcer):
    """
    Парсер файла "Выработка продукции"
    """

    def __init__(self, excel_file: InMemoryUploadedFile, user_id: int) -> None:
        super().__init__(
            excel_file,
            excel_config=ProductionProductExcelConfig,
            columns_identifier=ProductionProductColumns,
            skiprows=ProductionProductExcelConfig.START_ROW,
            dtype={col.name: str for col in ProductionProductColumns},
            sheet_name=[str(number).zfill(2) for number in range(1, 13)],
        )
        ProductionProductValidator.is_empty_file(self._df)
        self.user_id = user_id
        self._filter()
        self.indicators: pl.DataFrame = None
        self.installations: pl.DataFrame = None
        self.types_plan: pl.DataFrame = None
        self.user_column_names = self._get_user_column_names(
            ProductionProductColumns,
            ["ПП М03", "Сетевой график (СГ)", "ФАКТ", "ФАКТ-ПП М03", "ФАКТ-СГ"],
        )

    def _filter(self, types=None) -> pl.DataFrame:
        """
        Фильтр необходимых данных по параметрам

        Returns:
            dataframe (pl.DataFrame): отфильтрованные данные
        """

        self._df: pl.DataFrame = self._df.select(
            [
                pl.when(pl.col(column) == "nan")
                .then(None)
                .otherwise(pl.col(column))
                .alias(column)
                for column in self._df.columns
                if column != "DATE"
            ]
            + ["DATE"]
        )

        self._df = self._df.filter(
            pl.col(ProductionProductColumns.INDICATOR_ID.name).is_not_null()
            | pl.col(ProductionProductColumns.PP_M03.name).is_not_null()
        )

        self._df = self._df.select(
            [pl.all().exclude("DATE").str.strip_chars().str.to_lowercase()] + ["DATE"]
        )

    def _validate(self, types=None) -> list[Optional[dict]]:
        """
        Валидация входных данных

        Returns:
            err_list (Optional[list[PresentationDataForError]]): перечень ошибок для пользователя
        """

        err_list: list[Optional[PresentationDataForError]] = []
        validator = ProductionProductValidator()

        self.indicators = HandbookLoader.get_handbook(GSIndicator)
        self.installations = HandbookLoader.get_handbook(GSInstallation)
        self.types_plan = HandbookLoader.get_handbook(GSTypePlan)

        indicators = ValidationData(
            data=self.__get_indicators(),
            loader=self.indicators,
            column_identificator=ProductionProductColumns.INDICATOR_ID.name,
            name_handbook_for_user="Показатель",
        )
        installations = ValidationData(
            data=self.__get_installations(),
            loader=self.installations,
            column_identificator=ProductionProductColumns.INDICATOR_ID.name,
            name_handbook_for_user="Установка",
        )
        types_plan = ValidationData(
            data=self.__get_type_plan(),
            loader=self.types_plan,
            column_identificator=ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name,
            name_handbook_for_user="Тип плана",
        )

        validations_list = [indicators, installations, types_plan]
        for validation_data in validations_list:
            err_list = validator.validate_input_fields(
                validation_data.data,
                validation_data.loader,
                validation_data.column_identificator,
                validation_data.name_handbook_for_user,
            )

        return [ob.__dict__ for ob in err_list]

    def _preprocess(self, types=None) -> pl.DataFrame:
        """
        Предобработка входных данных

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        self.__select_installations()
        self.__replace_header()
        self.__convert_data_to_db()

    def create_records(self) -> pl.DataFrame:
        """
        Генерация таблицы для преобразования в объекты django

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        self._preprocess()

        indicators = DataFrameData(
            loader=self.indicators,
            column_identificator=ProductionProductColumns.INDICATOR_ID.name,
        )
        installations = DataFrameData(
            loader=self.installations,
            column_identificator=ProductionProductColumnsLoadDB.INSTALLATION_ID.name,
        )
        types_plan = DataFrameData(
            loader=self.types_plan,
            column_identificator=ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name,
        )
        data_list = [indicators, installations, types_plan]
        for data in data_list:
            self._df = self.__replace_value_columns_by_id(
                data.loader,
                data.column_identificator,
            )

        return self._df.with_columns(pl.lit(self.user_id).alias("created_by_id"))

    def _perform_data(self, data: dict, dtype: dict | None) -> pd.DataFrame:
        """
        Обрабатывает датафрейм пандас, подготавливая его к конвертации в датафрейм поларс

        Args:
            data (dict): загруженные данные
            dtype (dict): типы данных для колонок

        Returns:
            dataframe (pd.DataFrame): преобразованные данные
        """

        current_year = datetime.now().year

        df_list: list[pd.DataFrame] = [
            v.assign(DATE=datetime(current_year, int(k), 1)) for k, v in data.items()
        ]

        pandas_df: pd.DataFrame = pd.concat(df_list, ignore_index=True)

        return super()._perform_data(pandas_df, dtype)

    def __get_type_plan(self) -> pl.DataFrame:
        """
        Получение наименований "Тип плана"

        Returns:
            dataframe (pl.DataFrame): данные по Типам плана
        """

        return (
            self._df.filter(
                (pl.col(ProductionProductColumns.INDICATOR_ID.name).is_null())
            )
            .select(
                pl.all().exclude([ProductionProductColumns.INDICATOR_ID.name, "DATE"])
            )
            .filter(~pl.all_horizontal(pl.all().is_in([None, "0"])))
            .unpivot(value_name=ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name)
            .unique(subset=ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name)
            .select(ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name)
        )

    def __get_installations(self) -> pl.DataFrame:
        """
        Получение наименований "Установок"

        Returns:
            dataframe (pl.DataFrame): данные по Установкам
        """

        return (
            self._df.filter(
                (
                    pl.col(
                        ProductionProductColumns.DIFFERENCE_FACT_NETWORK_GRAPH.name
                    ).is_null()
                )
                & (pl.col(ProductionProductColumns.INDICATOR_ID.name).is_not_null())
            )
            .select(pl.col(ProductionProductColumns.INDICATOR_ID.name))
            .unique()
        )

    def __get_indicators(self) -> pl.DataFrame:
        """
        Получение наименований "Показателей"

        Returns:
            dataframe (pl.DataFrame): данные по Показателям
        """

        return (
            self._df.filter(
                (
                    pl.col(
                        ProductionProductColumns.DIFFERENCE_FACT_NETWORK_GRAPH.name
                    ).is_not_null()
                )
                & (pl.col(ProductionProductColumns.INDICATOR_ID.name).is_not_null())
            )
            .select(pl.col(ProductionProductColumns.INDICATOR_ID.name))
            .unique()
        )

    def __select_installations(self) -> pl.DataFrame:
        """
        Выделить установки в отдельную колонку

        Returns:
            dataframe (pl.DataFrame): данные по Установкам
        """

        types_plan_df = self._df.select(
            pl.all().exclude(ProductionProductColumns.INDICATOR_ID.name)
        )
        indicators_installations_df = self._df.select(
            pl.col(ProductionProductColumns.INDICATOR_ID.name)
        )

        installations_name: list = self.__get_installations()[
            ProductionProductColumns.INDICATOR_ID.name
        ]

        indicators_installations_df = indicators_installations_df.with_columns(
            pl.when(
                pl.col(ProductionProductColumns.INDICATOR_ID.name).is_in(
                    installations_name
                )
            )
            .then(pl.col(ProductionProductColumns.INDICATOR_ID.name))
            .otherwise(None)
            .alias(ProductionProductColumnsLoadDB.INSTALLATION_ID.name)
        )
        indicators_installations_df = indicators_installations_df.with_columns(
            pl.col(ProductionProductColumnsLoadDB.INSTALLATION_ID.name).forward_fill()
        )

        self._df = pl.concat(
            [indicators_installations_df, types_plan_df], how="horizontal"
        ).filter(
            ~pl.col(ProductionProductColumns.INDICATOR_ID.name).is_in(
                installations_name
            )
            | pl.col(ProductionProductColumns.INDICATOR_ID.name).is_null()
        )

    def __replace_header(self) -> pl.DataFrame:
        """
        Замена шапки

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        types_plan_df = self._df.select(
            pl.all().exclude(
                [
                    ProductionProductColumns.INDICATOR_ID.name,
                    ProductionProductColumnsLoadDB.INSTALLATION_ID.name,
                    "DATE",
                ]
            )
        )
        new_headers = types_plan_df.row(0)
        types_plan_df.columns = new_headers

        indicator_installations_df = self._df.select(
            [
                pl.col(ProductionProductColumns.INDICATOR_ID.name),
                ProductionProductColumnsLoadDB.INSTALLATION_ID.name,
                "DATE",
            ]
        )

        self._df = pl.concat(
            [indicator_installations_df, types_plan_df], how="horizontal"
        ).filter(pl.col(ProductionProductColumns.INDICATOR_ID.name).is_not_null())

    def __convert_data_to_db(self):
        """
        Преобразование датафрейма в формат для загрузки в БД

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        self._df = self._df.unpivot(
            index=[
                ProductionProductColumns.INDICATOR_ID.name,
                ProductionProductColumnsLoadDB.INSTALLATION_ID.name,
                "DATE",
            ],
            value_name=ProductionProductColumnsLoadDB.VALUE.name,
            variable_name=ProductionProductColumnsLoadDB.TYPE_PLAN_ID.name,
        )

    def __replace_value_columns_by_id(
        self,
        loader: pl.DataFrame,
        column_df: str,
    ) -> pl.DataFrame:
        """
        Замена значений колонок на ID

        Args:
            loader (pl.DataFrame): выгруженный справочник
            column_df (str): наименование колонки данных их файла

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        merge_df = self._df.join(
            loader,
            left_on=column_df,
            right_on="name",
        )

        return merge_df.with_columns(pl.col("id").alias(column_df)).drop("id")
