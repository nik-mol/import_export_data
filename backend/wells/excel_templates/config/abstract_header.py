from enum import Enum
from typing import Optional


class DefaultStyleHeader(Enum):
    """
    Стили по умолчанию
    """

    BORDER_PARAMS = {
        "top": {"border_style": "thin", "color": "000000"},
        "left": {"border_style": "thin", "color": "000000"},
        "bottom": {"border_style": "thin", "color": "000000"},
        "right": {"border_style": "thin", "color": "000000"},
    }
    ALIGMENT = {"horizontal": "center", "vertical": "center", "wrap_text": True}
    FONT_STYLE = {
        "color": "000000",
        "name": "Calibri",
        "size": "11",
    }


class AbstractWorkSheetHeader:
    """
    Класс для шапки таблицы отчетов по фонду ИНК с базовыми колонками
    """

    @classmethod
    def get_column(cls, column_name: str, row_number: int = 1) -> Optional[dict]:
        """
        Получить базовую колонку

        Args:
            row_number (int): номер строки

        Returns:
            dict: колонока с данными
        """

        base_columns = {
            "DISTRICT": {
                "column": 1,
                "row": row_number,
                "text": "УН",
                "column_width": 20,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
            "FIELD": {
                "column": 2,
                "row": row_number,
                "text": "Мест-е",
                "column_width": 20,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
            "NUMBER": {
                "column": 3,
                "row": row_number,
                "text": "Номер",
                "column_width": 10,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
            "WELL": {
                "column": 4,
                "row": row_number,
                "text": "Скв.",
                "column_width": 12,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
            "PAD": {
                "column": 5,
                "row": row_number,
                "text": "КП",
                "column_width": 12,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
            "DATE_FUND": {
                "column": 6,
                "row": row_number,
                "text": "",
                "column_width": 13,
                "font_style": DefaultStyleHeader.FONT_STYLE.value,
                "cell_style": {
                    "aligment": DefaultStyleHeader.ALIGMENT.value,
                    "border": DefaultStyleHeader.BORDER_PARAMS.value,
                },
            },
        }

        return base_columns.get(column_name)
