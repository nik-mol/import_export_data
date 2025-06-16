from django.urls import path

from .views import ExportCalculationTemporaryPeriodView

app_name = "wells"


urlpatterns = [
    path(
        "characteristic/temporary_period/export",
        ExportCalculationTemporaryPeriodView.as_view(),
        name="characteristic-temporary-export",
    ),
]
