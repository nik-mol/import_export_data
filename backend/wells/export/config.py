from dataclasses import dataclass
from enum import Enum

import numpy as np


@dataclass
class SheetExcelData:
    """
    Параметры для выгрузки отчета по временным приостановкам из ФОНДа ИНК
    """

    wells_loader: np.ndarray
    sheet_name: str
