from django_filters.rest_framework import FilterSet
from gas_service.models import GSProductionProduct


class GSProductionProductListFilter(FilterSet):
    """
    Фильтр "Выработки продукции"
    """

    class Meta:
        model = GSProductionProduct
        fields = ["indicator", "installation", "type_plan", "date"]
