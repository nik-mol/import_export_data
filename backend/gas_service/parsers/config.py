from dataclasses import dataclass

import polars as pl
from common.enums import DictedEnum
from common.parcer.abstract import AbstractParcerConfig


class ProductionProductExcelConfig(AbstractParcerConfig):
    """
    Конфигуратор загрузки файла "Выработка продукции"
    """

    START_ROW = 3


class ProductionProductColumns(DictedEnum):
    """
    Идентификатор колонок для файла "Выработка продукции"
    """

    INDICATOR_ID = 2
    PP_M03 = 3
    NETWORK_GRAPH = 4
    FACT = 5
    DIFFERENCE_FACT_PP_M03 = 6
    DIFFERENCE_FACT_NETWORK_GRAPH = 7


class ProductionProductColumnsLoadDB(DictedEnum):
    """
    Наименования колонок для загрузки в БД файла "Выработка продукции"
    """

    INSTALLATION_ID = "installation_id"
    TYPE_PLAN_ID = "type_plan_id"
    VALUE = "value"


class HandbookColumns(DictedEnum):
    """
    Наименования колонок для загрузки справочников
    """

    INDICATOR_ID = 0
    INSTALLATION_ID = 1
    TYPE_PLAN_ID = 2


@dataclass
class ValidationData:
    """
    Параметры для валидации наименований
    """

    data: pl.DataFrame = None
    loader: pl.DataFrame = None
    column_identificator: str = ""
    name_handbook_for_user: str = ""


@dataclass
class DataFrameData:
    """
    Параметры для преобразования датафрейма
    """

    data: pl.DataFrame = None
    loader: pl.DataFrame = None
    column_identificator: str = ""
