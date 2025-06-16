from enum import Enum
from typing import Optional


class AbstractExtendedEnum(Enum):
    """
    Базовая абстрактная расширенная версия энума
    """

    @classmethod
    def as_dict(cls) -> dict:
        """
        Преобразовать энум в словарь
        """
        return {i.name: i.value for i in cls}

    @classmethod
    def get_keys(cls):
        """
        Преобразовать ключи энума в список
        """
        return list(cls.as_dict().keys())

    @classmethod
    def get_values(cls):
        """
        Преобразовать значения энума в список
        """
        return list(cls.as_dict().values())

    @classmethod
    def transform(cls) -> Enum:
        """
        Метод трансформирует энум в новый энум

        Для чего это нужно -

        У нас есть базовый энум

        class Enum(Enum):
            prop: 1
            prop1: 2
            prop3: 3

        И мы хотим сделать новый энум для него, но только вида

        class Enum(Enum):
            prop: 1
            prop3: 3

        но при этом чтобы была возможность использовать ключи старого энума.
        Данный метод пересобирает заново базовый энум в новый с учетом измененных ключей
        """
        dict_to_transform = {}
        for index, value in enumerate(cls):
            dict_to_transform[value.name] = index

        return Enum("Default", dict_to_transform)


class DictedEnum(AbstractExtendedEnum):
    """
    Расширенный энум, с возможностью преобразования данных в словарь
    """

    @classmethod
    def list(cls, values_to_remove: Optional[list] = None):
        """
        Преобразовать ключи в список
        """
        list_data = list(map(lambda x: x.value, cls))
        if values_to_remove:
            for item in values_to_remove:
                list_data.remove(item)
        return list_data
