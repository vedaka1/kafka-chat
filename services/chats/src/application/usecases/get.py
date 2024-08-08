from dataclasses import dataclass

from src.api.v1.schemas import ListPaginatedResponse, PaginationOutSchema
from src.application.commands.chats import GetChatsListCommand
from src.domain.chats.entities import Chat
from src.domain.chats.service import BaseChatService


@dataclass
class GetChatsListUseCase:
    chat_service: BaseChatService

    async def execute(
        self, command: GetChatsListCommand
    ) -> ListPaginatedResponse[Chat]:

        chats = await self.chat_service.find_many(
            limit=command.pagination.limit,
            offset=command.pagination.offset,
            search=command.search,
        )
        count = await self.chat_service.count_many(search=command.search)
        return ListPaginatedResponse(
            items=chats,
            pagination=PaginationOutSchema(
                limit=command.pagination.limit,
                offset=command.pagination.offset,
                total=count,
            ),
        )
