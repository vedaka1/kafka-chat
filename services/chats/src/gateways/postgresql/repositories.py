import uuid
from dataclasses import asdict, dataclass

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.chats.entities import Chat
from src.domain.chats.repository import BaseChatRepository
from src.gateways.postgresql.models import ChatModel


@dataclass
class ChatRepository(BaseChatRepository):
    session: AsyncSession

    async def create(self, chat: Chat) -> None:
        query = insert(ChatModel).values(asdict(chat))
        await self.session.execute(query)
        return None

    async def delete(self, id: uuid.UUID) -> None:
        query = delete(ChatModel).where(ChatModel.id == id)
        await self.session.execute(query)
        return None

    async def update(self, chat: Chat) -> None:
        query = (
            update(ChatModel).where(ChatModel.id == chat.id).values(title=chat.title)
        )
        await self.session.execute(query)
        return None

    async def get_by_id(self, id: uuid.UUID) -> Chat | None:
        query = select(ChatModel).where(ChatModel.id == id)
        result = await self.session.execute(query)
        chat = result.scalar_one_or_none()
        return (
            Chat(
                id=chat.id,
                owner_id=chat.owner_id,
                title=chat.title,
                created_at=chat.created_at,
            )
            if chat
            else None
        )

    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[Chat]:
        if search:
            query = (
                select(ChatModel)
                .where(
                    ChatModel.title.ilike(
                        "%{0}%".format(r"%%".join(search.lower().split()))
                    )
                )
                .limit(limit)
                .offset(offset)
            )
        else:
            query = select(ChatModel).limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            Chat(
                id=chat.id,
                owner_id=chat.owner_id,
                title=chat.title,
                created_at=chat.created_at,
            )
            for chat in result.scalars().all()
        ]

    async def count_many(self, search: str | None = None) -> int:
        if search:
            query = (
                select(func.count())
                .select_from(ChatModel)
                .where(
                    ChatModel.title.ilike(
                        "%{0}%".format(r"%%".join(search.lower().split()))
                    )
                )
            )
        else:
            query = select(func.count()).select_from(ChatModel)
        result = await self.session.execute(query)
        count = result.scalars().one_or_none()
        if not count:
            return 0
        return count
