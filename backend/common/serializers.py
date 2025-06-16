"""
Общие сериализаторы
"""

from typing import Any

from rest_framework import serializers


class CeleryTaskIdSerializer(serializers.Serializer[Any]):
    """
    Сериализатор вывода экселя
    """

    task_id = serializers.CharField(help_text="Id задачи")


class FileRetrieveSerializer(serializers.Serializer[Any]):
    """
    Сериализатор скачивания файла
    """

    file = serializers.FileField(help_text="Файл")
