from rest_framework.exceptions import APIException


class EmptyFile(APIException):
    """
    Импорт пустого файла
    """

    status_code = 400
    default_detail = "В загруженном файле нет данных"
    default_code = "service_unavailable"
