from common.exaptions import EmptyFileLoaded, NoFileUploaded
from django.core.files.uploadedfile import InMemoryUploadedFile


class FileImportValidator:
    @staticmethod
    def does_file_exists(func):
        """
        Декоратор для валидации наличия файла в запросе
        """

        def wrap(view, request, *args, **kwargs):
            try:
                request.data["file"]
            except KeyError:
                raise NoFileUploaded
            return func(view, request, *args, **kwargs)

        return wrap

    @staticmethod
    def is_file_valid(func):
        """
        Декоратор для проверки, что передан не пустой файл
        """

        def wrap(view, request, *args, **kwargs):
            file_loaded: InMemoryUploadedFile = request.data["file"]
            if isinstance(file_loaded, str):
                raise EmptyFileLoaded

            return func(view, request, *args, **kwargs)

        return wrap
