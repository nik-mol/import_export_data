from enum import Enum

from common.excel_templates.base import ExcelWorkSheet
from wells.excel_templates.config.description_sheets import (
    DescriptionHeadersTemporaryPeriod,
)
from wells.excel_templates.config.temporary_period import WorkSheetHeaderTemporaryPeriod


class DefaultStyleTemporaryPeriod(Enum):
    """
    Стили по умолчанию
    """

    FONT_STYLE = {
        "color": "000000",
        "name": "Calibri",
        "size": "11",
    }


class AbstractTemporaryPeriodWorkSheet(ExcelWorkSheet):
    """
    Абстрактный класс для описания листов по временным приостановкам из ФОНДа ИНК
    """

    header = WorkSheetHeaderTemporaryPeriod.get_filtered_headers(
        DescriptionHeadersTemporaryPeriod.BASE_HEADERS.value,
        DescriptionHeadersTemporaryPeriod.HEADERS_TEMPORARY_PERIOD.value,
    )
    additional_styles = [
        {
            "param_definition": "row_dimensions",
            "param_definition_index": 4,
            "key": "height",
            "value": "45",
        },
    ]

    @staticmethod
    def create_worksheet_seal(description: str) -> list[dict]:
        """
        Создание переменной для описвания листа

        Args:
            description (str): описание листа

        Returns:
            list[dict]: список параметров для записи в эксель
        """

        return [
            {
                "column": 1,
                "row": 1,
                "text": description,
                "font_style": DefaultStyleTemporaryPeriod.FONT_STYLE.value,
            }
        ]
