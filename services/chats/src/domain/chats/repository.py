from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.domain.chats.entities import Chat


@dataclass
class BaseChatRepository(ABC):

    @abstractmethod
    async def create(self, chat: Chat) -> None:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass

    @abstractmethod
    async def update(self, chat: Chat) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Chat | None:
        pass

    @abstractmethod
    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[Chat]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass
