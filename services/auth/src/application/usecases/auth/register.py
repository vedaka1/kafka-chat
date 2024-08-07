import logging
from dataclasses import dataclass

from src.application.common.password_hasher import BasePasswordHasher
from src.application.common.transaction import BaseTransactionManager
from src.application.contracts.commands.user import RegisterCommand
from src.domain.events.auth import NewUserRegistered
from src.domain.exceptions.user import UserAlreadyExistsException
from src.domain.users.repository import (
    BaseUserConfirmationRepository,
    BaseUserRepository,
)
from src.domain.users.user import User, UserConfirmation
from src.infrastructure.message_broker.base import BaseMessageBroker
from src.infrastructure.message_broker.converters import convert_event_to_broker_message

logger = logging.getLogger()


@dataclass
class RegisterUseCase:
    password_hasher: BasePasswordHasher
    user_repository: BaseUserRepository
    user_confirmation_repository: BaseUserConfirmationRepository
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
        user_confirmation = UserConfirmation.create(user_id=user.id)
        await self.user_confirmation_repository.create(user_confirmation)
        event = NewUserRegistered(
            email=user.email,
            message_text="Here is the link to confirm your account<br>",
            confirmation_link="<a href='http://localhost/api/v1/auth/confirmation?id={0}&code={1}'>Confirm</a>".format(
                user_confirmation.id, user_confirmation.code
            ),
        )
        try:
            await self.message_broker.send_message(
                topic=self.broker_topic,
                value=convert_event_to_broker_message(event),
                key=str(event.id).encode(),
            )
        except Exception as e:
            logger.error("Failed to send message to broker: {0}".format(e))

        await self.transaction_manager.commit()
        return None
