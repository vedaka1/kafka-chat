from dataclasses import dataclass
from typing import Any

from src.application.common.password_hasher import BasePasswordHasher
from src.application.common.transaction import BaseTransactionManager
from src.application.contracts.commands.user import RegisterCommand
from src.domain.exceptions.user import UserAlreadyExistsException
from src.domain.users.repository import BaseUserRepository
from src.domain.users.user import User


@dataclass
class RegisterUseCase:
    user_repository: BaseUserRepository
    password_hasher: BasePasswordHasher
    transaction_manager: BaseTransactionManager

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
        await self.transaction_manager.commit()
        return None
