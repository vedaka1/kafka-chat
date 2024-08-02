import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities import User


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
