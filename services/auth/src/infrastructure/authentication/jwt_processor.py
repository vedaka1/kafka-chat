import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from src.application.common.jwt_processor import BaseJwtTokenProcessor
from src.infrastructure.config import settings


@dataclass
class JwtTokenProcessor(BaseJwtTokenProcessor):
    def generate_token(self, user_id: UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
        )
        return f"Bearer {encoded_jwt}"

    def validate_token(self, token: str) -> UUID | None:
        try:
            payload = jwt.decode(
                token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM]
            )
            user_id = payload.get("sub")
            return UUID(user_id)
        except (JWTError, ValueError, KeyError):
            return None
