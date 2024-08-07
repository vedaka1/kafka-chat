from dataclasses import dataclass

from .base import ApplicationException


@dataclass(eq=False, init=False)
class UserIsNotAuthorizedException(ApplicationException):
    status_code: int = 401
    message: str = "Not authorized"


@dataclass(eq=False, init=False)
class TokenExpiredException(ApplicationException):
    status_code: int = 401
    message: str = "Your access token has expired"
