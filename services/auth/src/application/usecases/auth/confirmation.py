from dataclasses import dataclass

from src.domain.users.repository import BaseUserRepository
from src.infrastructure.message_broker.base import BaseMessageBroker


@dataclass
class UserConfirmationUseCase:

    async def execute(self):
        pass
