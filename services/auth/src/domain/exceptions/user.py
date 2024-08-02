from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class UserNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "User not found"


@dataclass(eq=False, init=False)
class UserInvalidCredentialsException(ApplicationException):
    status_code: int = 404
    message: str = "Email or password is incorrect"


@dataclass(eq=False, init=False)
class UserIsNotAuthorizedException(ApplicationException):
    status_code: int = 404
    message: str = "You are not authorized"


@dataclass(eq=False, init=False)
class UserAlreadyExistsException(ApplicationException):
    status_code: int = 400
    message: str = "User already exists"