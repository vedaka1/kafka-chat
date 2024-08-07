import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime

from src.domain.users.entities import Friends, User
from src.gateways.postgresql.models import FriendsModel, UserModel


class BaseDto(ABC):
    def dump(self):
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: dict) -> "BaseDto":
        pass


@dataclass
class UserDto(BaseDto):
    id: uuid.UUID | None
    username: str
    hashed_password: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4()

    @staticmethod
    def load(data: dict) -> "UserDto":
        return UserDto(
            id=data.get("id"),
            username=data.get("username"),
            hashed_password=data.get("hashed_password"),
            email=data.get("email"),
            is_active=data.get("is_active"),
            is_verified=data.get("is_verified"),
            is_superuser=data.get("is_superuser"),
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            email=self.email,
            is_active=self.is_active,
            is_verified=self.is_verified,
            is_superuser=self.is_superuser,
        )

    @staticmethod
    def from_entity(entity: User | UserModel) -> "UserDto":
        return UserDto(
            id=entity.id,
            username=entity.username,
            hashed_password=entity.hashed_password,
            email=entity.email,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            is_superuser=entity.is_superuser,
        )


@dataclass
class FriendsDto(BaseDto):
    id: int | None
    user_id: uuid.UUID
    friend_id: uuid.UUID
    created_at: datetime

    @staticmethod
    def load(data: dict) -> "FriendsDto":
        return FriendsDto(
            id=data.get("id"),
            user_id=data.get("user_id"),
            friend_id=data.get("friend_id"),
            created_at=data.get("created_at"),
        )

    def to_entity(self) -> Friends:
        return Friends(
            id=self.id,
            user_id=self.user_id,
            friend_id=self.friend_id,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(entity: Friends | FriendsModel) -> "FriendsDto":
        return FriendsDto(
            id=entity.id,
            user_id=entity.user_id,
            friend_id=entity.friend_id,
            created_at=entity.created_at,
        )
