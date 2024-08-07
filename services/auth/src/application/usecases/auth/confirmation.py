from dataclasses import dataclass
from datetime import datetime

from src.application.common.transaction import BaseTransactionManager
from src.application.contracts.commands.user import UserConfirmationCommand
from src.domain.exceptions.user import (
    UserConfirmationCodeExpired,
    UserConfirmationCodeInvalid,
    UserConfirmationCodeNotFound,
    UserNotFoundException,
)
from src.domain.users.repository import (
    BaseUserConfirmationRepository,
    BaseUserRepository,
)


@dataclass
class UserConfirmationUseCase:
    user_repository: BaseUserRepository
    user_confirmation_repository: BaseUserConfirmationRepository
    transaction_manager: BaseTransactionManager

    async def execute(self, command: UserConfirmationCommand) -> None:
        confirmation = await self.user_confirmation_repository.get_by_id(command.id)
        if not confirmation:
            raise UserConfirmationCodeNotFound
        if confirmation.expired_at < datetime.now():
            raise UserConfirmationCodeExpired
        if confirmation.code != command.code:
            raise UserConfirmationCodeInvalid
        user = await self.user_repository.get_by_id(confirmation.user_id)
        if not user:
            raise UserNotFoundException
        user.is_verified = True
        await self.user_repository.update(confirmation.user_id, user)
        await self.user_confirmation_repository.delete(confirmation.id)
        await self.transaction_manager.commit()
        return None
