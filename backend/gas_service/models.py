from common.models import DomainModel

# Create your models here.
from django.db import models


class GSIndicator(DomainModel):
    """
    Модель, описывающая справочник "Показатель"
    """

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Наименование",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Показатель"
        verbose_name_plural = "Показатели"


class GSInstallation(DomainModel):
    """
    Модель, описывающая справочник "Установка"
    """

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Наименование",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Установка"
        verbose_name_plural = "Установки"


class GSTypePlan(DomainModel):
    """
    Модель, описывающая справочник "Тип плана"
    """

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Наименование",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип плана"
        verbose_name_plural = "Типы плана"


class GSProductionProduct(DomainModel):
    """
    Модель для хранения данных по выработке продукции
    """

    date = models.DateField(
        verbose_name="Дата, первое число месяца",
    )
    indicator = models.ForeignKey(
        to=GSIndicator,
        on_delete=models.CASCADE,
        verbose_name="Показатель",
        related_name="production_product_indicator",
    )
    installation = models.ForeignKey(
        to=GSInstallation,
        on_delete=models.CASCADE,
        verbose_name="Установка",
        related_name="production_product_installation",
    )
    type_plan = models.ForeignKey(
        to=GSTypePlan,
        on_delete=models.CASCADE,
        verbose_name="Тип плана",
        related_name="production_product_type_plan",
    )
    value = models.FloatField(
        null=True,
        verbose_name="Значение выработки продукции",
    )

    class Meta:
        verbose_name = "Выработка продукции"
        verbose_name_plural = "Выработки продукции"
