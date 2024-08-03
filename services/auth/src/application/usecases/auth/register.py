import logging
from dataclasses import dataclass

from src.application.common.password_hasher import BasePasswordHasher
from src.application.common.transaction import BaseTransactionManager
from src.application.contracts.commands.user import RegisterCommand
from src.domain.events.auth import NewUserRegistered
from src.domain.exceptions.user import UserAlreadyExistsException
from src.domain.users.repository import BaseUserRepository
from src.domain.users.user import User
from src.infrastructure.message_broker.base import BaseMessageBroker
from src.infrastructure.message_broker.converters import convert_event_to_broker_message

logger = logging.getLogger()


@dataclass
class RegisterUseCase:
    user_repository: BaseUserRepository
    password_hasher: BasePasswordHasher
    user_repository: BaseUserRepository
    message_broker: BaseMessageBroker
    transaction_manager: BaseTransactionManager
    broker_topic = "notifications"

    async def execute(self, command: RegisterCommand) -> None:
        user_exists = await self.user_repository.get_by_email(command.email)
        if user_exists:
            raise UserAlreadyExistsException
        hashed_password = self.password_hasher.hash(command.password)
        user = User.create(
            username=command.username,
            hashed_password=hashed_password,
            email=command.email,
        )
        await self.user_repository.create(user)
        event = NewUserRegistered(email=user.email, confirmation_link="test")
        try:
            await self.message_broker.send_message(
                topic=self.broker_topic,
                value=convert_event_to_broker_message(event),
                key=str(event.id).encode(),
            )
        except Exception as e:
            logger.error(e)

        await self.transaction_manager.commit()
        return None
