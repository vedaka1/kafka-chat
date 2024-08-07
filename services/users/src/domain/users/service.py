import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.users.entities import Friends, User


@dataclass
class BaseUserService(ABC):
    @abstractmethod
    async def update(self, id: uuid.UUID, user: User) -> None:
        pass

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> User:
        pass

    @abstractmethod
    async def find_many(
        self, offset: int, limit: int, search: str | None = None
    ) -> list[User]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass


@dataclass
class BaseFriendsService(ABC):
    abstractmethod

    async def create(self, friends: Friends) -> None:
        pass

    @abstractmethod
    async def update(self, id: int, friends: Friends) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Friends:
        pass

    @abstractmethod
    async def get_by_user_id(
        self, user_id: uuid.UUID, offset: int, limit: int
    ) -> list[Friends]:
        pass

    @abstractmethod
    async def get_by_user_and_friend_id(
        self, user_id: uuid.UUID, friend_id: uuid.UUID
    ) -> Friends | None:
        pass

    # @abstractmethod
    # async def find_many(
    #     self, offset: int, limit: int, search: str | None = None
    # ) -> list[Friends]:
    #     pass

    @abstractmethod
    async def count_many(self, user_id: uuid.UUID) -> int:
        pass
