import uuid
from dataclasses import dataclass

from src.application.contracts.common.pagination import PaginationQuery
from src.domain.users.user import User


@dataclass
class RegisterCommand:
    username: str
    password: str
    email: str


@dataclass
class LoginCommand:
    password: str
    username: str


@dataclass
class GetUserCommand:
    user_id: uuid.UUID


@dataclass
class DeleteUserCommand:
    user_id: uuid.UUID


@dataclass
class UpdateUserCommand:
    user_id: uuid.UUID
    user: User


@dataclass
class GetUsersListCommand:
    pagiantion: PaginationQuery
