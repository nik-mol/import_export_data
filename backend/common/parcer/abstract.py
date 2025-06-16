from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union

import pandas as pd
import polars as pl
from common.enums import DictedEnum
from common.parcer.utils import ExcelProcessor


@dataclass
class AbstractParcerConfig:
    """
    Абстракция энума, не было проблем с типами
    """

    START_ROW = 0


class Parcer(metaclass=ABCMeta):
    """
    Абстрактный класс парсера

    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
    """

    @abstractmethod
    def __init__(
        self,
        excel_file,
        excel_config: type[AbstractParcerConfig],
        columns_identifier: type[DictedEnum],
        excel_processor: type[ExcelProcessor],
        **kwargs,
    ) -> None:
        self._df = excel_processor.load_data(
            excel_file=excel_file,
            skiprows=excel_config.START_ROW,
            usecols=columns_identifier.get_values(),
            **kwargs,
        )
        self.user_column_names = self._get_user_column_names(
            columns_identifier, self._get_user_columns_list(self._df)
        )
        self._df = self._rename_file_columns(self._df, columns_identifier)

    @abstractmethod
    def _preprocess(self, types: DictedEnum):
        """
        Фильтр необходимых данных по параметрам
        """
        raise NotImplementedError()

    @abstractmethod
    def _validate(self, types: Optional[DictedEnum] = None):
        """
        Валидация входных данных
        """
        raise NotImplementedError()

    @abstractmethod
    def _filter(self, types: Optional[DictedEnum] = None):
        """
        Фильтр необходимых данных по параметрам
        """
        raise NotImplementedError()

    @abstractmethod
    def create_records(self, *args, **kwargs):
        """
        Генерация таблицы для преобразования в объекты django
        """
        pass

    def _get_user_columns_list(
        self, df: Union[pd.DataFrame, dict[str, pd.DataFrame]]
    ) -> list[str]:
        """
        Получение списка первоначальных названий колонок
        """

        # если передается pd.DataFrame
        if isinstance(df, pd.DataFrame):
            return df.columns.tolist()
        # если передается словарь из множества датафреймов
        dfloc = next(iter(df.values()))
        return dfloc.columns.tolist()

    def _get_user_column_names(
        self, columns: type[DictedEnum], user_columns: list[str]
    ) -> dict[int, str]:
        """
        Метод отдает словарь {номер столбца: название столбца}
        """

        return {key: value for key, value in zip(columns.get_values(), user_columns)}

    def _rename_file_columns(
        self,
        df: Union[pd.DataFrame, dict[str, pd.DataFrame]],
        enum_cols: type[DictedEnum],
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Переименовывание колонок датафрейма, либо всех датафреймов
        """
        # если передается pd.DataFrame
        if isinstance(df, pd.DataFrame):
            return self.__rename_df_columns(df, enum_cols)
        # если передается словарь из множества датафреймов
        if all(isinstance(value, pd.DataFrame) for value in df.values()):
            return {
                key: self.__rename_df_columns(value, enum_cols)
                for key, value in df.items()
            }
        else:
            raise ValueError("Значения в словаре должны быть DataFrame")

    def __rename_df_columns(
        self, df: pd.DataFrame, enum_cols: type[DictedEnum]
    ) -> pd.DataFrame:
        """
        Переименовывание колонок
        Нужно, чтобы была возможность сохранить оригинальные названия
        """
        return df.rename(
            columns={
                df.columns[idx]: value
                for idx, value in zip(range(len(df.columns)), enum_cols.get_keys())
            }
        )


class PolarsParcer(Parcer):
    """
    Парсер на основе polars
    """

    @abstractmethod
    def __init__(
        self,
        excel_file,
        excel_config: type[AbstractParcerConfig],
        columns_identifier: type[DictedEnum] | None = None,
        excel_processor=ExcelProcessor,
        lazy: bool = False,
        dtype: dict | type | None = None,
        skiprows: int = 0,
        drop_rows: list | int | None = None,
        **kwargs,
    ) -> None:
        # может оказаться так, что изначально непонятно, сколько колонок
        # в файле, из-за динамичной структуры файла
        if columns_identifier is not None:
            usecols = columns_identifier.get_values()
        else:
            usecols = None

        pandas_df = excel_processor.load_data(
            excel_file=excel_file,
            engine="openpyxl",
            skiprows=skiprows,
            usecols=usecols,
            **kwargs,
        )

        if drop_rows is not None:
            pandas_df = pandas_df.drop(index=drop_rows)

        if columns_identifier:
            self.user_column_names = self._get_user_column_names(
                columns_identifier, self._get_user_columns_list(pandas_df)
            )
            pandas_df = self._rename_file_columns(pandas_df, columns_identifier)
        pandas_df = self._perform_data(pandas_df, dtype)

        self._df = pl.LazyFrame(pandas_df) if lazy else pl.from_pandas(pandas_df)

    def _perform_data(cls, df: pd.DataFrame, dtype: dict | type | None) -> pd.DataFrame:
        """
        Обрабатывает датафрейм пандас, подготавливая его к конвертации в датафрейм поларс
        """

        # Этот костыль нужен, потому что поларс, считывая пандас, может криво расставить типы в колонках
        if dtype is not None:
            df = df.astype(dtype)

        return df
