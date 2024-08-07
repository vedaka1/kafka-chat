import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: uuid.UUID
    username: str
    hashed_password: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool


@dataclass
class Friends:
    id: int | None
    user_id: uuid.UUID
    friend_id: uuid.UUID
    created_at: datetime

    @staticmethod
    def create(user_id: uuid.UUID, friend_id: uuid.UUID) -> "Friends":
        return Friends(
            id=None, user_id=user_id, friend_id=friend_id, created_at=datetime.now()
        )
