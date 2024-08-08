from dataclasses import dataclass
from uuid import UUID

from src.domain.chats.entities import Chat
from src.domain.chats.repository import BaseChatRepository
from src.domain.chats.service import BaseChatService
from src.domain.exceptions.chats import ChatNotFoundException


@dataclass
class ChatService(BaseChatService):
    chat_repository: BaseChatRepository

    async def create(self, chat: Chat) -> None:
        await self.chat_repository.create(chat)
        return None

    async def delete(self, id: UUID) -> None:
        await self.get_by_id(id=id)
        await self.chat_repository.delete(id=id)
        return None

    async def update(self, chat: Chat) -> None:
        await self.get_by_id(id=chat.id)
        await self.chat_repository.update(chat)
        return None

    async def get_by_id(self, id: UUID) -> Chat | None:
        chat = await self.chat_repository.get_by_id(id)
        if not chat:
            raise ChatNotFoundException
        return chat

    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[Chat]:
        chats = await self.chat_repository.find_many(
            offset=offset, limit=limit, search=search
        )
        return chats

    async def count_many(self, search: str | None = None) -> int:
        return await self.chat_repository.count_many(search=search)
