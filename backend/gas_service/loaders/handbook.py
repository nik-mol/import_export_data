import polars as pl
from common.creator import DefaultCreator
from gas_service.models import GSIndicator, GSInstallation, GSTypePlan


class IndicatorLoader(DefaultCreator):
    """
    Класс для загрузки данных в справочник "Показатель"
    """

    def create_instances(self, data: pl.DataFrame) -> None:
        """
        Метод для создания списка инстансов

        Args:
            data pl.DataFrame: датафрейм для Справочника
        """

        return self.save_instances_to_db(GSIndicator, data.to_dicts())


class InstallationLoader(DefaultCreator):
    """
    Класс для загрузки данных в справочник "Установка"
    """

    def create_instances(self, data: pl.DataFrame) -> None:
        """
        Метод для создания списка инстансов

        Args:
            data pl.DataFrame: датафрейм для Справочника
        """

        return self.save_instances_to_db(GSInstallation, data.to_dicts())


class TypePlanLoader(DefaultCreator):
    """
    Класс для загрузки данных в справочник "Тип плана"
    """

    def create_instances(self, data: pl.DataFrame) -> None:
        """
        Метод для создания списка инстансов

        Args:
            data pl.DataFrame: датафрейм для Справочника
        """

        return self.save_instances_to_db(GSTypePlan, data.to_dicts())
