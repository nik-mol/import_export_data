from io import BytesIO

import pandas as pd
from rest_framework.exceptions import APIException


class ExcelProcessor:
    """
    Дефолтный класс для обработки экселек
    """

    @staticmethod
    def load_data(excel_file: BytesIO, **kwargs) -> pd.DataFrame:
        try:
            if isinstance(excel_file, bytes):
                return pd.read_excel(BytesIO(excel_file), **kwargs)
            else:
                return pd.read_excel(excel_file, **kwargs)
        except ValueError as exc:
            # Нет листа
            raise APIException(
                f"В форме отсутствует лист {kwargs['sheet_name']}"
            ) from exc
