from django.contrib.auth.models import User
from django.db import models


class RoleUserModel(models.Model):
    """
    Поля пользователя создавшего модель
    """

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        verbose_name="Пользователь, создавший запись",
        null=True,
        blank=True,
        # делается для того, чтобы django не создавало для User обратную связь
        related_name="+",
    )

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    """
    Поля создания и обновления модели
    """

    created_datetime = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True,
        verbose_name="Отметка времени создания объекта",
    )
    updated_datetime = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
        verbose_name="Отметка времени изменения объекта",
    )

    class Meta:
        abstract = True


class DomainModel(RoleUserModel, TimestampedModel):
    """
    Общие поля для объектов доменной модели
    """

    class Meta:
        abstract = True
