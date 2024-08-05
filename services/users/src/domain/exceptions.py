from dataclasses import dataclass


@dataclass(eq=False, init=False)
class ApplicationException(Exception):
    status_code: int = 500
    message: str = "An unknown error occurred"

    def __init__(self, *args, **kwargs):
        return super().__init__(self.message, *args, **kwargs)


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
