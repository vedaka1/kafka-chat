from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.chats.entities import Chat
from src.domain.messages.entities import Message
from src.gateways.postgresql.models import ChatModel, FriendsModel, UserModel


class BaseDto(ABC):
    def dump(self):
        return asdict(self)

    @staticmethod
    @abstractmethod
    def load(data: dict) -> "BaseDto":
        pass


@dataclass
class ChatDto(BaseDto):
    id: UUID | None
    owner_id: UUID
    title: str
    created_at: datetime

    def __post_init__(self):
        if not self.id:
            self.id = uuid4()

    @staticmethod
    def load(data: dict) -> "ChatDto":
        return ChatDto(
            id=data.get("id"),
            owner_id=data.get("owner_id"),
            title=data.get("title"),
            created_at=data.get("created_at"),
        )

    def to_entity(self) -> Chat:
        return Chat(
            id=self.id,
            owner_id=self.owner_id,
            title=self.title,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(entity: Chat | ChatModel) -> "ChatDto":
        return ChatDto(
            id=entity.id,
            owner_id=entity.owner_id,
            title=entity.title,
            created_at=entity.created_at,
        )


@dataclass
class FriendsDto(BaseDto):
    id: int | None
    user_id: UUID
    friend_id: UUID
    created_at: datetime

    @staticmethod
    def load(data: dict) -> "FriendsDto":
        return FriendsDto(
            id=data.get("id"),
            user_id=data.get("user_id"),
            friend_id=data.get("friend_id"),
            created_at=data.get("created_at"),
        )

    # def to_entity(self) -> Friends:
    #     return Friends(
    #         id=self.id,
    #         user_id=self.user_id,
    #         friend_id=self.friend_id,
    #         created_at=self.created_at,
    #     )

    # @staticmethod
    # def from_entity(entity: Friends | FriendsModel) -> "FriendsDto":
    #     return FriendsDto(
    #         id=entity.id,
    #         user_id=entity.user_id,
    #         friend_id=entity.friend_id,
    #         created_at=entity.created_at,
    #     )
