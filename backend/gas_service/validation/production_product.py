from typing import Optional

import polars as pl
from common.validation_errors import PresentationDataForError
from gas_service.exceptions import EmptyFile


class ProductionProductValidator:
    """
    Кдасс для валидации импорта "Выработка продукции"
    """

    def __init__(self) -> None:
        self.errors: list = []

    def validate_input_fields(
        self,
        data: pl.DataFrame,
        loader: pl.DataFrame,
        column_identificator: str,
        name_handbook_for_user: str,
    ) -> list[Optional[PresentationDataForError]]:
        """
        Проверка входных данных на соответсвие справочникам

        Args:
            data (pl.DataFrame): данные из файла
            loader (pl.DataFrame): выгруженный справочник
            name_handbook_for_user (str): наименование справочника

        Returns:
            err_list (Optional[list[PresentationDataForError]]): перечень ошибок для пользователя
        """

        merged_data = data.join(
            loader,
            left_on=column_identificator,
            right_on="name",
            how="left",
        )

        invalid_data = merged_data.filter(pl.col("id").is_null())[column_identificator]
        for value in invalid_data:
            self.errors.append(
                PresentationDataForError(
                    type="Ошибка",
                    column=name_handbook_for_user,
                    text=f"Наименование '{value}' отсутвует в справочнике '{name_handbook_for_user}'",
                    name_object="",
                )
            )

        return self.errors

    @staticmethod
    def is_empty_file(df: pl.DataFrame) -> None:
        """
        Валидация на не пустой файл

        Args:
            dataframe (pl.DataFrame): данные
        Raises:
            EmptyFile: в загруженном файле нет данных
        """

        if df.is_empty():
            raise EmptyFile
