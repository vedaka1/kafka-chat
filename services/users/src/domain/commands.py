import uuid
from dataclasses import dataclass

from src.api.v1.schemas import PaginationQuery
from src.domain.entities import User


@dataclass
class GetUserCommand:
    user_id: uuid.UUID


@dataclass
class UpdateUserCommand:
    user_id: uuid.UUID
    user: User


@dataclass
class GetUsersListCommand:
    search: str | None
    pagiantion: PaginationQuery
