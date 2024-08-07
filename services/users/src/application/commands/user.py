import uuid
from dataclasses import dataclass

from src.api.v1.schemas import PaginationQuery
from src.domain.users.entities import User


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


@dataclass
class GetUserFriendsListCommand:
    # user_id: uuid.UUID
    pagiantion: PaginationQuery


@dataclass
class AddFriendCommand:
    friend_id: uuid.UUID


@dataclass
class DeleteFriendCommand:
    friend_id: uuid.UUID
