from common.models import DomainModel
from django.db import models


class FundList(models.IntegerChoices):
    """
    Перечисление с названиями фондов
    """

    VDZ = 0, "ВДЗ"
    VZ = 1, "ВЗ"
    GD = 2, "ГД"
    GN = 3, "ГН"
    ND = 4, "НД"
    NN = 5, "НН"
    POGL = 6, "ПОГЛ"
    RD = 7, "РД"
    RN = 8, "РН"


class WellsStatuses(models.Model):
    """
    Статусы состояний скважин
    """

    name = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Имя статуса"
    )
    guid_1c = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="ИД статуса в 1C"
    )
    alt_name = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Псевдоним"
    )

    class Meta:
        verbose_name = "Статусы скважин"
        verbose_name_plural = "Статусы скважин"

    def __str__(self) -> str:
        return f"{self.name}"


class WellsStatus(DomainModel):
    """
    Справочник по статусам скважин
    """

    name = models.CharField(max_length=255, verbose_name="Имя статуса скважины")
    color = models.CharField(max_length=255, verbose_name="Цвет", default="#ffffffff")
    fund = models.IntegerField(
        choices=FundList.choices,
        default=4,
    )
    status = models.ForeignKey(
        to=WellsStatuses, on_delete=models.DO_NOTHING, verbose_name="Состояние скважины"
    )
    is_actual = models.BooleanField(
        default=True, verbose_name="Актуален статус скважины или нет"
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Справочник по статусам скважин"
        verbose_name_plural = "Справочник по статусам скважин"
        constraints = [
            models.UniqueConstraint(fields=["name", "fund"], name="unique_name_fund")
        ]


class District(DomainModel):
    """
    Участок недр / лицензионный участок
    """

    name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Наименование", unique=True
    )
    short_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Сокращенное наименование"
    )
    alt_name = models.CharField(max_length=200, null=True, verbose_name="Псевдоним")
    name_1c = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Имя в 1с"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Участок недр"
        verbose_name_plural = "Участки недр"


class Field(DomainModel):
    """
    Месторождение
    """

    name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Наименование", unique=True
    )
    short_name = models.CharField(
        null=True, blank=True, max_length=255, verbose_name="Сокращенное наименование"
    )
    alt_name = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Псевдоним"
    )
    name_1c = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="Имя в 1с"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Месторождение"
        verbose_name_plural = "Месторождения"


class Pad(DomainModel):
    """
    Кустовая площадка управления геологии
    Эта сущность хранит в себе только имена скважин и ссылки на справочник
    """

    name = models.CharField(max_length=100, verbose_name="Название")
    create_date = models.DateField(verbose_name="Дата создания", auto_now=True)
    field = models.ForeignKey(
        to=Field,
        on_delete=models.DO_NOTHING,
        verbose_name="Месторождение",
        null=True,
        blank=True,
    )
    deleted = models.BooleanField(verbose_name="Флаг удаления", null=True, blank=True)
    license = models.ForeignKey(
        to=District, on_delete=models.DO_NOTHING, verbose_name="Участок недр"
    )

    is_numberless = models.BooleanField(
        verbose_name="Признак безномерного куста", default=False
    )

    def __str__(self) -> str:
        return f"{self.field}, {self.license}, {self.name}"

    class Meta:
        verbose_name = "Кустовая площака"
        verbose_name_plural = "Кустовые площадки"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "field", "license"], name="unique_pad_name"
            )
        ]


class Well(DomainModel):
    """
    Скважина Управления геологии
    Эта сущность хранит в себе только имена скважин и ссылки на справочник
    """

    name = models.CharField(max_length=100, verbose_name="Имя скважины", unique=True)
    wellpad = models.ForeignKey(
        to=Pad,
        on_delete=models.DO_NOTHING,
        verbose_name="Кустовая площадка",
    )
    is_numberless = models.BooleanField(
        verbose_name="Признак безномерной скважины", default=False
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Скважина"
        verbose_name_plural = "Скважины"


class CharacteristicBaseFund(DomainModel):
    """
    Модель постоянных характеристик для фонда скважин ИНК
    """

    well = models.OneToOneField(
        to=Well,
        related_name="fund_well",
        on_delete=models.CASCADE,
        verbose_name="Ссылка на скважину",
    )
    original_well = models.ForeignKey(
        Well,
        null=True,
        on_delete=models.CASCADE,
        related_name="fund_original_well",
        verbose_name="Первоначальный номер скважины",
    )
    area = models.CharField(null=True, verbose_name="Площадь")
    delay_period = models.DateField(
        null=True, verbose_name="Срок временной приостановки"
    )
    delay_start = models.DateField(
        null=True, verbose_name="Дата начала временной приостановки"
    )
    building_end_date = models.DateField(
        null=True, verbose_name="Дата окончания строительста"
    )
    building_end_date_zbs = models.DateField(
        null=True, verbose_name="Дата окончания строительста ЗБС"
    )
    conservation_date_fact = models.DateField(
        null=True, verbose_name="Дата начала фактической консвервации / ликвидации "
    )
    conservation_date_start = models.DateField(
        null=True, verbose_name="Дата начала консервации / ликвидации (РТН)"
    )
    conservation_date_end = models.DateField(
        null=True, verbose_name="Дата окончания консервации / ликвидации (РТН)"
    )
    delay_comment = models.TextField(
        null=True, verbose_name="Комментарий по сроку временной приостановки"
    )
    conservation_comment = models.TextField(
        null=True, verbose_name="Комментарий для консервации"
    )
    inspection_date_fact = models.DateField(
        null=True, verbose_name="Дата осмотра (факт)"
    )
    inspection_date_chart = models.DateField(
        null=True, verbose_name="Дата осмотра (график)"
    )
    inspection_date_next_year = models.DateField(
        null=True, verbose_name="Дата осмотра в следующем году"
    )

    def __str__(self) -> str:
        return f"{self.id}, {self.well}"

    class Meta:
        verbose_name = "Постоянные характеристики"
        verbose_name_plural = "Постоянные характеристики"


class WellsBaseFund(DomainModel):
    """
    Фонд скважин ИНК
    """

    date = models.DateField(verbose_name="Дата состояния")
    well = models.ForeignKey(
        to=Well,
        on_delete=models.CASCADE,
        verbose_name="Ссылка на скважину",
    )
    status = models.ForeignKey(
        to=WellsStatus, on_delete=models.DO_NOTHING, verbose_name="Категория"
    )

    def __str__(self) -> str:
        return f"{self.well}, {self.date}"

    class Meta:
        verbose_name = "Фонд ИНК"
        verbose_name_plural = "Фонд ИНК"
        constraints = [
            models.UniqueConstraint(fields=["date", "well"], name="unique_date_well")
        ]
