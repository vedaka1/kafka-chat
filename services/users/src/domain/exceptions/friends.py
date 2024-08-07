from dataclasses import dataclass

from .base import ApplicationException


@dataclass(eq=False, init=False)
class AlreadyFriendsException(ApplicationException):
    status_code: int = 409
    message: str = "You are already friends"


@dataclass(eq=False, init=False)
class FriendNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Friend not found"
