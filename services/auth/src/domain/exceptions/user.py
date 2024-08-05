from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False, init=False)
class UserNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "User not found"


@dataclass(eq=False, init=False)
class UserInvalidCredentialsException(ApplicationException):
    status_code: int = 400
    message: str = "Email or password is incorrect"


@dataclass(eq=False, init=False)
class UserIsNotAuthorizedException(ApplicationException):
    status_code: int = 401
    message: str = "Not authorized"


@dataclass(eq=False, init=False)
class UserAlreadyExistsException(ApplicationException):
    status_code: int = 409
    message: str = "User already exists"


@dataclass(eq=False, init=False)
class TokenExpiredException(ApplicationException):
    status_code: int = 401
    message: str = "Your access token has expired"


@dataclass(eq=False, init=False)
class UserConfirmationCodeNotFound(ApplicationException):
    status_code: int = 404
    message: str = "User confirmation code not found"


@dataclass(eq=False, init=False)
class UserConfirmationCodeExpired(ApplicationException):
    status_code: int = 401
    message: str = "Your confirmation code has expired"


@dataclass(eq=False, init=False)
class UserConfirmationCodeInvalid(ApplicationException):
    status_code: int = 400
    message: str = "Your confirmation code is invalid"
