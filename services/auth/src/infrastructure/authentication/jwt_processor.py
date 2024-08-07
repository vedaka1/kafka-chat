from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from src.application.common.jwt_processor import BaseJwtTokenProcessor
from src.domain.exceptions.base import ApplicationException
from src.domain.exceptions.user import TokenExpiredException
from src.infrastructure.settings import settings


@dataclass
class JwtTokenProcessor(BaseJwtTokenProcessor):
    def generate_token(self, user_id: UUID) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt.PRIVATE_KEY, algorithm=settings.jwt.ALGORITHM
        )
        return f"Bearer {encoded_jwt}"

    def validate_token(self, token: str) -> UUID | None:
        """Returns a user id from token"""
        try:
            payload = jwt.decode(
                token,
                settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            user_id = payload.get("sub")
            if datetime.fromtimestamp(payload.get("exp")) <= datetime.now():
                raise TokenExpiredException
            return UUID(user_id)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException
