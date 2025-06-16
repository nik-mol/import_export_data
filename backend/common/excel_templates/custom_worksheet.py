from typing import Any

from openpyxl.cell import Cell, WriteOnlyCell
from openpyxl.worksheet._write_only import WriteOnlyWorksheet


class CustomWorkSheet(WriteOnlyWorksheet):
    """
    Класс переопределяющий Worksheet из openpyxl
    Нужен чтобы оптимизировать скорость выгрузки Excel
    """

    def __init__(self, parent, title) -> None:
        super().__init__(parent, title)
        self._virtual_cells: dict[tuple, Any] = {}

    def append(self, row: list, **kwargs):
        """
        Добавление строки в файл

        Args:
            row (_type_): массив данных
            **kwargs: параметры для добавленных ячеек
        """
        self._max_row += 1
        self._max_col = max(self._max_col, len(row))  # type: ignore[has-type]
        is_object_cell = len(kwargs) > 0
        for column, cell in enumerate(row):
            new_cell = cell
            if is_object_cell is True:
                new_cell = WriteOnlyCell(self, cell)
                for k, v in kwargs.items():
                    setattr(new_cell, k, v)
            self._virtual_cells[(self._max_row, column + 1)] = new_cell

    def cell(self, row, column, value=None):
        """
        Получение и изменение значения ячейки

        Args:
            row (int): строка
            column (int): колонка
            value (_type_, optional): новое значение. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            _type_: ячейка
        """
        if row < 1 or column < 1:
            raise ValueError("Row or column values must be at least 1")

        if (row, column) in self._virtual_cells:
            cell = self._virtual_cells[(row, column)]
            if not isinstance(cell, Cell):
                if value is None:
                    cell = WriteOnlyCell(self, cell)
                else:
                    cell = value
                self._virtual_cells[(row, column)] = cell
            elif value is not None:
                cell.value = value
        else:
            self._max_row = max(self._max_row, row)
            self._max_col = max(self._max_col, column)
            if value is None:
                cell = WriteOnlyCell(self, None)
            else:
                cell = value
            self._virtual_cells[(row, column)] = cell

        return cell
