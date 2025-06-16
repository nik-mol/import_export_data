from gas_service.models import (
    GSIndicator,
    GSInstallation,
    GSProductionProduct,
    GSTypePlan,
)
from rest_framework import serializers


class GSIndicatorSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для справочника "Показатель"
    """

    class Meta:
        model = GSIndicator
        fields = ["id", "name", "created_by"]


class GSInstallationSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для справочника "Установка"
    """

    class Meta:
        model = GSInstallation
        fields = ["id", "name", "created_by"]


class GSTypePlanSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для справочника "Тип плана"
    """

    class Meta:
        model = GSTypePlan
        fields = ["id", "name", "created_by"]


class GSProductionProductSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для "Выработки продукции"
    """

    indicator_name = serializers.CharField(read_only=True, source="indicator.name")
    installation_name = serializers.CharField(
        read_only=True, source="installation.name"
    )
    type_plan_name = serializers.CharField(read_only=True, source="type_plan.name")

    class Meta:
        model = GSProductionProduct
        fields = [
            "id",
            "date",
            "indicator",
            "installation",
            "type_plan",
            "indicator_name",
            "installation_name",
            "type_plan_name",
            "value",
            "created_by",
        ]
