from django.urls import path
from gas_service.views import (
    GSIndicatorCreateView,
    GSIndicatorListView,
    GSIndicatorSingleView,
    GSInstallationCreateView,
    GSInstallationListView,
    GSInstallationSingleView,
    GSProductionProductCreateView,
    GSProductionProductListView,
    GSProductionProductSingleView,
    GSTypePlanCreateView,
    GSTypePlanListView,
    GSTypePlanSingleView,
    ImportHandbookView,
    ImportProductionProductView,
)

app_name = "gas_service"

urlpatterns = [
    path("indicator/list", GSIndicatorListView.as_view(), name="indicator"),
    path("indicator", GSIndicatorCreateView.as_view(), name="indicator-new"),
    path(
        "indicator/<int:pk>", GSIndicatorSingleView.as_view(), name="indicator-single"
    ),
    path("installation/list", GSInstallationListView.as_view(), name="installation"),
    path("installation", GSInstallationCreateView.as_view(), name="installation-new"),
    path(
        "installation/<int:pk>",
        GSInstallationSingleView.as_view(),
        name="installation-single",
    ),
    path("typeplan/list", GSTypePlanListView.as_view(), name="typeplan"),
    path("typeplan", GSTypePlanCreateView.as_view(), name="typeplan-new"),
    path("typeplan/<int:pk>", GSTypePlanSingleView.as_view(), name="typeplan-single"),
    path(
        "productionproduct/list",
        GSProductionProductListView.as_view(),
        name="productionproduct",
    ),
    path(
        "productionproduct",
        GSProductionProductCreateView.as_view(),
        name="productionproduct-new",
    ),
    path(
        "productionproduct/<int:pk>",
        GSProductionProductSingleView.as_view(),
        name="productionproduct-single",
    ),
    path("import/handbook", ImportHandbookView.as_view(), name="import-handbook"),
    path(
        "import/productionproduct",
        ImportProductionProductView.as_view(),
        name="import-productionproduct",
    ),
]
