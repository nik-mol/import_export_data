from rest_framework import serializers


class ExportCalculationTemporaryPeriodQuerySerializer(serializers.Serializer):
    """
    Сериализатор параметров экспорта отчета по временным приостановкам из ФОНДа ИНК
    """

    input_date = serializers.DateField(
        required=False,
        default=None,
        help_text="Дата для формирования листа 'вывод из вр приост' в формате 'ГГГГ-ММ-01'",
        input_formats=["%Y-%m-01"],
    )
