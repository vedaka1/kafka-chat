from dataclasses import dataclass
from uuid import UUID

from src.application.commands.chats import CreateChatCommand
from src.domain.chats.entities import Chat
from src.domain.chats.service import BaseChatService
from src.gateways.postgresql.transaction import BaseTransactionManager


@dataclass
class CreateChatUseCase:
    chat_service: BaseChatService
    transaction_manager: BaseTransactionManager

    async def execute(self, user_id: UUID, command: CreateChatCommand) -> None:
        chat = Chat.create(owner_id=user_id, title=command.title)
        await self.chat_service.create(chat)
        await self.transaction_manager.commit()
        return None
