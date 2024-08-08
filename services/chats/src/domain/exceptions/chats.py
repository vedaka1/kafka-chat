from dataclasses import dataclass

from .base import ApplicationException


@dataclass(eq=False, init=False)
class ChatNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Chat not found"
