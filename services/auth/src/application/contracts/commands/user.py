import uuid
from dataclasses import dataclass

from pydantic import BaseModel, EmailStr

from src.application.contracts.common.pagination import PaginationQuery
from src.domain.users.user import User


@dataclass
class RegisterCommand(BaseModel):
    username: str
    password: str
    email: EmailStr


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


@dataclass
class UserConfirmationCommand:
    id: uuid.UUID
    code: uuid.UUID
