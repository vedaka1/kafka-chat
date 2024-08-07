import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.gateways.postgresql.dto import FriendsDto, UserDto


@dataclass
class BaseUserRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def create(self, user: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def update(self, user: UserDto) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> UserDto | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDto]:
        pass

    @abstractmethod
    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[UserDto]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass


@dataclass
class BaseFriendsRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def create(self, friends: FriendsDto) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def update(self, friends: FriendsDto) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> FriendsDto | None:
        pass

    @abstractmethod
    async def get_by_user_id(
        self, user_id: uuid.UUID, offset: int, limit: int
    ) -> list[FriendsDto]:
        pass

    @abstractmethod
    async def get_by_user_and_friend_id(
        self, user_id: uuid.UUID, friend_id: uuid.UUID
    ) -> FriendsDto | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[FriendsDto]:
        pass

    # @abstractmethod
    # async def find_many(
    #     self,
    #     limit: int = 10,
    #     offset: int = 0,
    #     search: str | None = None,
    # ) -> list[UserDto]:
    #     pass

    @abstractmethod
    async def count_many(self, user_id: uuid.UUID) -> int:
        pass
