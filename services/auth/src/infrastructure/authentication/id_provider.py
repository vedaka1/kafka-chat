import uuid
from dataclasses import dataclass

from src.application.common.id_provider import BaseIdProvider
from src.application.common.jwt_processor import BaseJwtTokenProcessor
from src.domain.exceptions.user import UserIsNotAuthorizedException


@dataclass
class JwtTokenIdProvider(BaseIdProvider):
    token_processor: BaseJwtTokenProcessor
    token: str

    def get_current_user_id(self, *, token: str = "") -> uuid.UUID:
        user_id = self.token_processor.validate_token(token if token else self.token)
        if user_id is None:
            raise UserIsNotAuthorizedException

        return user_id
