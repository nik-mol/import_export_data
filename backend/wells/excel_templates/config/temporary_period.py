from common.enums import DictedEnum
from wells.excel_templates.config.abstract_header import (
    AbstractWorkSheetHeader,
    DefaultStyleHeader,
)
from wells.excel_templates.config.description_sheets import TemporaryPeriodHeadersConfig


class WorkSheetHeaderTemporaryPeriod(DictedEnum):
    """
    Шапка таблицы отчета по временным приостановкам из ФОНДа ИНК
    """

    DISTRICT = (
        AbstractWorkSheetHeader.get_column(
            "DISTRICT", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )
    FIELD = (
        AbstractWorkSheetHeader.get_column(
            "FIELD", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )
    NUMBER = (
        AbstractWorkSheetHeader.get_column(
            "NUMBER", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )
    WELL = (
        AbstractWorkSheetHeader.get_column(
            "WELL", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )
    PAD = (
        AbstractWorkSheetHeader.get_column(
            "PAD", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )
    DATE_FUND = (
        AbstractWorkSheetHeader.get_column(
            "DATE_FUND", TemporaryPeriodHeadersConfig.ROW.value
        ),
    )

    BUILDING_END_DATE = (
        {
            "column": 7,
            "row": 4,
            "text": "Дата окончания строительства",
            "column_width": 15,
            "font_style": DefaultStyleHeader.FONT_STYLE.value,
            "cell_style": {
                "aligment": DefaultStyleHeader.ALIGMENT.value,
                "border": DefaultStyleHeader.BORDER_PARAMS.value,
            },
        },
    )
    DELAY_PERIOD = (
        {
            "column": 8,
            "row": 4,
            "text": "срок вр_приост",
            "column_width": 15,
            "font_style": DefaultStyleHeader.FONT_STYLE.value,
            "cell_style": {
                "aligment": DefaultStyleHeader.ALIGMENT.value,
                "border": DefaultStyleHeader.BORDER_PARAMS.value,
            },
        },
    )
    DELAY_START = (
        {
            "column": 9,
            "row": 4,
            "text": "Дата начала вр. приостановки",
            "column_width": 15,
            "font_style": DefaultStyleHeader.FONT_STYLE.value,
            "cell_style": {
                "aligment": DefaultStyleHeader.ALIGMENT.value,
                "border": DefaultStyleHeader.BORDER_PARAMS.value,
            },
        },
    )
    STATUS_PREVIOUS_MONTH = (
        {
            "column": 6,
            "row": 4,
            "text": "",
            "column_width": 14,
            "font_style": DefaultStyleHeader.FONT_STYLE.value,
            "cell_style": {
                "aligment": DefaultStyleHeader.ALIGMENT.value,
                "border": DefaultStyleHeader.BORDER_PARAMS.value,
            },
        },
    )
    STATUS_LAST_MONTH = (
        {
            "column": 7,
            "row": 4,
            "text": "",
            "column_width": 13,
            "font_style": DefaultStyleHeader.FONT_STYLE.value,
            "cell_style": {
                "aligment": DefaultStyleHeader.ALIGMENT.value,
                "border": DefaultStyleHeader.BORDER_PARAMS.value,
            },
        },
    )

    @classmethod
    def get_filtered_headers(
        cls, base_headers: list[str], additional_headers: list[str]
    ):
        """
        Фильтр заголовков

        Args:
            base_headers (list[str]): список базовых заголовков
            additional_headers (list[str]): список дополнительных заголовков

        Returns:
            отфильтрованные заголовки
        """

        result_headers: list[str] = base_headers + additional_headers

        return [header for header in cls if header.name in result_headers]
