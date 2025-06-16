from abc import abstractmethod
from functools import reduce

from django.db import models


class DefaultCreator:
    @abstractmethod
    def create_instances(self):
        """
        Метод для создания списка инстансов
        """
        raise NotImplementedError()

    def save_instances_to_db(
        self, django_model: models, objects_to_create, batch_size: int = 300
    ) -> None:
        """
        Метод для сохранения списка инстансов
        """
        return django_model.objects.bulk_create(
            [django_model(**vals) for vals in objects_to_create], batch_size=batch_size
        )

    def update_instances_to_db(
        self,
        django_model,
        objects_to_update,
        fields_to_update: list,
        batch_size: int = 300,
    ) -> None:
        """
        Метод для сохранения списка инстансов
        """
        django_model.objects.bulk_update(
            [django_model(**vals) for vals in objects_to_update],
            fields_to_update,
            batch_size=batch_size,
        )

    def delete_instances_to_db(self, django_model, objects_to_delete) -> None:
        """
        Метод для удаления списка инстансов
        """

        if len(objects_to_delete) == 0:
            return

        list_querysets = [
            django_model.objects.filter(**vals) for vals in objects_to_delete
        ]

        reduce(self.__reduce_function, list_querysets).delete()
