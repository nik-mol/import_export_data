from common.response import celery_response
from common.serializers import CeleryTaskIdSerializer
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from wells.serializers import ExportCalculationTemporaryPeriodQuerySerializer
from wells.tasks import export_calculation_temporary_period


class ExportCalculationTemporaryPeriodView(GenericAPIView):
    """
    Класс для выгрузки отчета по временным приостановкам из ФОНДа ИНК
    На выходе task_id
    """

    @extend_schema(
        summary="Выгрузка отчета по временным приостановкам из ФОНДа ИНК",
        parameters=[ExportCalculationTemporaryPeriodQuerySerializer],
        responses={
            200: CeleryTaskIdSerializer,
            404: OpenApiResponse(description="Произошла ошибка при выгрузке отчета"),
        },
    )
    def get(self, request: Request):
        serializer = ExportCalculationTemporaryPeriodQuerySerializer(
            data=request.query_params
        )
        serializer.is_valid(raise_exception=True)
        input_date = serializer.validated_data["input_date"]
        result = export_calculation_temporary_period.apply_async((input_date,))

        return celery_response(result.id)
