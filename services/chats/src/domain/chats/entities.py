from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Chat:
    id: UUID
    owner_id: UUID
    title: str
    created_at: datetime

    @staticmethod
    def create(owner_id: UUID, title: str) -> "Chat":
        return Chat(
            id=uuid4(),
            owner_id=owner_id,
            title=title,
            created_at=datetime.now(),
        )


@dataclass
class ChatMember:
    id: UUID
    chat_id: UUID
    user_id: UUID
    joined_at: datetime
    role: str

    @staticmethod
    def create(chat_id: UUID, user_id: str, *, role: str = "member") -> "ChatMember":
        return ChatMember(
            id=uuid4(),
            chat_id=chat_id,
            user_id=user_id,
            joined_at=datetime.now(),
            role=role,
        )


@dataclass
class ChatRole:
    name: str
