from rest_framework.exceptions import APIException


class NoFileUploaded(APIException):
    """
    При загрузке файла отсутсвует файл
    """

    status_code = 400
    default_detail = "В запросе отсутствует файл или параметр с именем file, хранящий в себе бинарник файла"
    default_code = "service_unavailable"


class EmptyFileLoaded(APIException):
    """
    В запросе не пришел файл внутри form-data
    """

    status_code = 400
    default_detail = "В запросе отсутствует файл"
    default_code = "service_unavailable"
