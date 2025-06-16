import polars as pl
from common.creator import DefaultCreator


class ProductionProductLoader(DefaultCreator):
    """
    Класс для создания инстансов из файла "Выработка продукции"
    """

    def create_instances(
        self,
        data: pl.DataFrame,
    ) -> list[dict]:
        """
        Метод для создания списка инстансов

        Args:
            data (pl.DataFrame): датафреймы из файла

        Returns:
            list[dict]: данные для записи в БД
        """

        return data.rename(str.lower).to_dicts()
