import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass

from src.domain.entities import User
from src.gateways.postgresql.models import UserModel


class BaseDto(ABC):
    def dump(self):
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: dict) -> "BaseDto":
        pass


@dataclass
class UserDto(BaseDto):
    id: uuid.UUID
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
            is_active=data["is_active"],
            is_verified=data["is_verified"],
            is_superuser=data["is_superuser"],
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
    def from_entity(entity: User) -> "UserDto":
        return UserDto(
            id=entity.id,
            username=entity.username,
            hashed_password=entity.hashed_password,
            email=entity.email,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            is_superuser=entity.is_superuser,
        )
