import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.exceptions.auth import UserIsNotAuthorizedException
from src.utils.jwt_processor import BaseJwtTokenProcessor


@dataclass
class BaseIdProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self, *, token: str) -> uuid.UUID: ...


@dataclass
class JwtTokenIdProvider(BaseIdProvider):
    token_processor: BaseJwtTokenProcessor
    token: str

    async def get_current_user_id(self, *, token: str = "") -> uuid.UUID:
        user_id = await self.token_processor.validate_token(
            token if token else self.token
        )
        if user_id is None:
            raise UserIsNotAuthorizedException

        return user_id
