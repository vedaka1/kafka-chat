from dataclasses import dataclass

from src.application.common.jwt_processor import BaseJwtTokenProcessor
from src.application.common.password_hasher import BasePasswordHasher
from src.application.common.transaction import BaseTransactionManager
from src.application.contracts.commands.user import LoginCommand
from src.application.contracts.responses.user import UserOut
from src.domain.common.token import Token
from src.domain.exceptions.user import *
from src.domain.users.repository import BaseUserRepository
from src.infrastructure.config import settings


@dataclass
class LoginUseCase:
    user_repository: BaseUserRepository
    password_hasher: BasePasswordHasher
    jwt_processor: BaseJwtTokenProcessor

    transaction_manager: BaseTransactionManager

    async def execute(self, command: LoginCommand) -> tuple[UserOut, Token]:
        user = await self.user_repository.get_by_email(command.username)
        if not user:
            raise UserInvalidCredentialsException
        if not self.password_hasher.verify(
            password=command.password, hash=user.hashed_password
        ):
            raise UserInvalidCredentialsException
        access_token = self.jwt_processor.generate_token(user.id)
        user_out = UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
        )
        token = Token(
            access_token=access_token,
            max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            token_type="access",
        )
        return user_out, token
