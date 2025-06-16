import os
from dataclasses import asdict

from celery import current_task, states
from common.response import celery_response
from common.serializers import CeleryTaskIdSerializer, FileRetrieveSerializer
from common.validation import FileImportValidator
from common.validation_errors import DataForResponse
from common.views import CreatedUserMixin, StaffPermission
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from gas_service.filters import GSProductionProductListFilter
from gas_service.loaders.handbook import (
    IndicatorLoader,
    InstallationLoader,
    TypePlanLoader,
)
from gas_service.loaders.production_product import ProductionProductLoader
from gas_service.models import (
    GSIndicator,
    GSInstallation,
    GSProductionProduct,
    GSTypePlan,
)
from gas_service.parsers.handbook import HandbookParcer
from gas_service.parsers.production_product import ProductionProductParcer
from gas_service.serializers import (
    GSIndicatorSerializer,
    GSInstallationSerializer,
    GSProductionProductSerializer,
    GSTypePlanSerializer,
)
from rest_framework import parsers
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.request import Request

from backend import celery_app


@extend_schema(summary="Вывод списка Показателей")
class GSIndicatorListView(ListAPIView):
    """
    Вывод списка "Показателей"
    """

    queryset = GSIndicator.objects.all()
    serializer_class = GSIndicatorSerializer


@extend_schema(summary="Создание Показателя")
class GSIndicatorCreateView(CreatedUserMixin, CreateAPIView):
    """
    Метод для создания "Показателя"
    """

    queryset = GSIndicator.objects.all()
    serializer_class = GSIndicatorSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Обновления/удаления/вывод Показателя")
class GSIndicatorSingleView(RetrieveUpdateDestroyAPIView):
    """
    Метод для обновления/удаления/вывода "Показателя"
    """

    queryset = GSIndicator.objects.all()
    serializer_class = GSIndicatorSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Вывод списка Установок")
class GSInstallationListView(ListAPIView):
    """
    Вывод списка "Установок"
    """

    queryset = GSInstallation.objects.all()
    serializer_class = GSInstallationSerializer


@extend_schema(summary="Создание Установки")
class GSInstallationCreateView(CreatedUserMixin, CreateAPIView):
    """
    Метод для создания "Установки"
    """

    queryset = GSInstallation.objects.all()
    serializer_class = GSInstallationSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Обновления/удаления/вывод Установки")
class GSInstallationSingleView(RetrieveUpdateDestroyAPIView):
    """
    Метод для обновления/удаления/вывода "Установок"
    """

    queryset = GSInstallation.objects.all()
    serializer_class = GSInstallationSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Вывод списка Типов плана")
class GSTypePlanListView(ListAPIView):
    """
    Вывод списка "Типов плана"
    """

    queryset = GSTypePlan.objects.all()
    serializer_class = GSTypePlanSerializer


@extend_schema(summary="Создание Типа плана")
class GSTypePlanCreateView(CreatedUserMixin, CreateAPIView):
    """
    Метод для создания "Типа плана"
    """

    queryset = GSTypePlan.objects.all()
    serializer_class = GSTypePlanSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Обновления/удаления/вывод Типа плана")
class GSTypePlanSingleView(RetrieveUpdateDestroyAPIView):
    """
    Метод для обновления/удаления/вывода "Типа плана"
    """

    queryset = GSTypePlan.objects.all()
    serializer_class = GSTypePlanSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Вывод списка Выработки продукции")
class GSProductionProductListView(ListAPIView):
    """
    Вывод списка "Выработки продукции"
    """

    queryset = GSProductionProduct.objects.select_related(
        "indicator", "installation", "type_plan"
    )
    serializer_class = GSProductionProductSerializer
    filterset_class = GSProductionProductListFilter


@extend_schema(summary="Создание Выработки продукции")
class GSProductionProductCreateView(CreatedUserMixin, CreateAPIView):
    """
    Метод для создания "Выработки продукции"
    """

    queryset = GSProductionProduct.objects.all()
    serializer_class = GSProductionProductSerializer
    permission_classes = [StaffPermission]


@extend_schema(summary="Обновления/удаления/вывод Выработки продукции")
class GSProductionProductSingleView(RetrieveUpdateDestroyAPIView):
    """
    Метод для обновления/удаления/вывода "Выработки продукции"
    """

    queryset = GSProductionProduct.objects.select_related(
        "indicator", "installation", "type_plan"
    )
    serializer_class = GSProductionProductSerializer
    permission_classes = [StaffPermission]


class ImportHandbookView(GenericAPIView):
    """
    Загрузка справочников (асинхронно)
    """

    serializer_class = FileRetrieveSerializer
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    permission_classes = [StaffPermission]

    @extend_schema(
        summary="Загрузка справочников",
        responses={
            200: CeleryTaskIdSerializer,
            404: OpenApiResponse(description="Произошла ошибка при загрузке файла"),
        },
    )
    @FileImportValidator.does_file_exists
    @FileImportValidator.is_file_valid
    def post(self, request: Request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_loaded: InMemoryUploadedFile = serializer.validated_data["file"]
        f = FileSystemStorage(location="files")
        name_file = f.save(file_loaded.name, file_loaded.file)

        result = self.load_async_handbook.apply_async(
            (str(f.path(name_file)), request.user.pk)
        )

        return celery_response(result.id)

    @staticmethod
    @celery_app.task
    def load_async_handbook(path: str, user_id: int):
        """
        Загрузка справочников"

        Args:
            file_content (BytesIO): файл
            user_id (int): ID пользователя
        """

        parser = HandbookParcer(path, user_id)
        (
            indicator_to_create,
            installation_to_create,
            type_plan_to_create,
        ) = parser.create_records()

        with transaction.atomic():
            loader = IndicatorLoader()
            loader.create_instances(indicator_to_create)
            loader = InstallationLoader()
            loader.create_instances(installation_to_create)
            loader = TypePlanLoader()
            loader.create_instances(type_plan_to_create)
            os.remove(path)


class ImportProductionProductView(GenericAPIView):
    """
    Импорт файла "Выработка продукции" (асинхронно)
    """

    serializer_class = FileRetrieveSerializer
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.FileUploadParser,
    )
    permission_classes = [StaffPermission]

    @extend_schema(
        summary="Импорт файла Выработка продукции",
        responses={
            200: CeleryTaskIdSerializer,
            404: OpenApiResponse(description="Произошла ошибка при загрузке файла"),
        },
    )
    @FileImportValidator.does_file_exists
    @FileImportValidator.is_file_valid
    def post(self, request: Request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_loaded: InMemoryUploadedFile = serializer.validated_data["file"]
        f = FileSystemStorage(location="files")
        name_file = f.save(file_loaded.name, file_loaded.file)

        result = self.load_async_production_product.apply_async(
            (str(f.path(name_file)), request.user.pk)
        )

        return celery_response(result.id)

    @staticmethod
    @celery_app.task
    def load_async_production_product(path: str, user_id: int):
        """
        Импорт файла "Выработка продукции"

        Args:
            file_content (BytesIO): файл
            user_id (int): ID пользователя
        """

        parser = ProductionProductParcer(path, user_id)
        errors = parser._validate()

        if not errors:
            loader = ProductionProductLoader()
            instanses_to_create = loader.create_instances(parser.create_records())
            with transaction.atomic():
                GSProductionProduct.objects.all().delete()
                loader.save_instances_to_db(GSProductionProduct, instanses_to_create)
            os.remove(path)
            output_response = asdict(
                DataForResponse(
                    warning=False,
                    text="Файл загружен",
                    log_errors=[],
                )
            )
            return current_task.update_state(
                state=states.SUCCESS,
                meta=output_response,
            )

        output_response = asdict(
            DataForResponse(
                warning=True,
                text="При загрузке обнаружены ошибки, исправьте их и загрузите файл снова",
                log_errors=errors,
            )
        )
        return current_task.update_state(
            state=states.SUCCESS,
            meta=output_response,
        )
