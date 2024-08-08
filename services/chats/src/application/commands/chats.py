from dataclasses import dataclass

from src.api.v1.schemas import PaginationQuery


@dataclass
class GetChatsListCommand:
    search: str | None
    pagination: PaginationQuery


@dataclass
class CreateChatCommand:
    title: str
