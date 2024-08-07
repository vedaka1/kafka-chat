import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

import aiohttp
import jwt

from src.domain.exceptions.auth import TokenExpiredException
from src.domain.exceptions.base import ApplicationException
from src.utils.common import cache_result


@dataclass
class BaseJwtTokenProcessor(ABC):
    @abstractmethod
    async def validate_token(self, token: str) -> uuid.UUID | None: ...


@cache_result
async def get_key() -> tuple[str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://auth:8000/api/v1/auth/certs") as response:
            data = await response.json()
            algorithm = data["data"]["alg"]
            pub_key = data["data"]["key"]
            return pub_key, algorithm


@dataclass
class JwtTokenProcessor(BaseJwtTokenProcessor):
    async def validate_token(self, token: str) -> UUID | None:
        """Returns a user id from token"""
        try:
            pub_key, algorithm = await get_key()
            payload = jwt.decode(
                token,
                pub_key,
                algorithms=[algorithm],
            )
            user_id = payload.get("sub")
            return UUID(user_id)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException
