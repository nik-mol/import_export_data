import polars as pl
from common.parcer.abstract import AbstractParcerConfig, PolarsParcer
from django.core.files.uploadedfile import InMemoryUploadedFile
from gas_service.exceptions import EmptyFile
from gas_service.models import GSIndicator, GSInstallation, GSTypePlan
from gas_service.parsers.config import HandbookColumns
from gas_service.queries import HandbookLoader


class HandbookParcer(PolarsParcer):
    """
    Парсер для загрузки Справочников
    """

    def __init__(self, excel_file: InMemoryUploadedFile, user_id: int) -> None:
        super().__init__(
            excel_file,
            excel_config=AbstractParcerConfig,
            columns_identifier=HandbookColumns,
            dtype=str,
        )
        self.user_id = user_id
        self._validate()
        self._filter()
        self._preprocess()

    def _filter(self, types=None) -> pl.DataFrame:
        """
        Фильтр необходимых данных по параметрам

        Returns:
            dataframe (pl.DataFrame): отфильтрованные данные
        """

        self._df: pl.DataFrame = self._df.filter(~pl.all_horizontal(pl.all().is_null()))

    def _validate(self, types=None):
        """
        Валидация входных данных

        Args:
            dataframe (pl.DataFrame): данные
        Raises:
            EmptyFile: в загруженном файле нет данных
        """

        if self._df.is_empty():
            raise EmptyFile

    def _preprocess(self, types=None) -> pl.DataFrame:
        """
        Предобработка входных данных

        Returns:
            dataframe (pl.DataFrame): преобразованные данные
        """

        self._df = self._df.select(
            [
                pl.col(column).str.strip_chars()
                if self._df[column].dtype == pl.String
                else pl.col(column)
                for column in self._df.columns
            ]
        )

    def create_records(self) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        """
        Генерация таблицы для преобразования в объекты django

        Returns:
            tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]: данные для записи в справочники
        """

        indicator_df = self.__get_data(HandbookColumns.INDICATOR_ID.name)
        installation_df = self.__get_data(HandbookColumns.INSTALLATION_ID.name)
        type_plan_df = self.__get_data(HandbookColumns.TYPE_PLAN_ID.name)

        indicator_to_create = HandbookParcer.select_data_missing_db(
            indicator_df,
            HandbookLoader.get_handbook(GSIndicator),
            HandbookColumns.INDICATOR_ID.name,
        )
        installation_to_create = HandbookParcer.select_data_missing_db(
            installation_df,
            HandbookLoader.get_handbook(GSInstallation),
            HandbookColumns.INSTALLATION_ID.name,
        )
        type_plan_to_create = HandbookParcer.select_data_missing_db(
            type_plan_df,
            HandbookLoader.get_handbook(GSTypePlan),
            HandbookColumns.TYPE_PLAN_ID.name,
        )

        return indicator_to_create, installation_to_create, type_plan_to_create

    def __get_data(self, column: str) -> pl.DataFrame:
        """
        Получение данных

        Args:
            column (str): наименование колонки

        Returns:
            dataframe (pl.DataFrame): данные для записи в справочники
        """

        return (
            self._df.filter((pl.col(column).is_not_null()))
            .select(pl.col(column))
            .unique()
            .with_columns(pl.lit(self.user_id).alias("created_by_id"))
        )

    @staticmethod
    def select_data_missing_db(
        data: pl.DataFrame, loader: pl.DataFrame, column: str
    ) -> pl.DataFrame:
        """
        Выбор данных отсутсвующих в справочнике

        Args:
            data (pl.DataFrame): данные из файла
            loader (pl.DataFrame): выгруженный справочник
            column (str): наименование колонки

        Returns:
            dataframe (pl.DataFrame): данные отсутвующие в справочнике
        """

        if data[column].dtype == pl.String:
            data = data.with_columns(
                (pl.col(column).str.to_lowercase()).alias("lower_column")
            )

            merged_data = data.join(
                loader,
                left_on="lower_column",
                right_on="name",
                how="left",
            ).rename({column: "name"})

            return merged_data.filter(pl.col("id").is_null()).drop(
                ["id", "lower_column"]
            )

        return pl.DataFrame(schema={"name": pl.String, "created_by_id": int})
