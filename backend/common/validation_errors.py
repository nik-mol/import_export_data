from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DataForResponse:
    """
    Класс для формирования ответа
    """

    text: Optional[str] = None
    log_errors: Optional[list] = field(default_factory=list)
    warning: bool = False


@dataclass
class PresentationDataForError:
    """
    Класс для храниения данных об ошибках и предупреждений
    """

    text: str
    type: Optional[str] = None
    column: Optional[str] = None
    name_object: Optional[str] = None
