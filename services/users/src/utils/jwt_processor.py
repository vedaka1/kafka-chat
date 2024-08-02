import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

import aiohttp
import jwt


@dataclass
class BaseJwtTokenProcessor(ABC):
    @abstractmethod
    def validate_token(self, token: str) -> uuid.UUID | None: ...


@dataclass
class JwtTokenProcessor(BaseJwtTokenProcessor):
    async def validate_token(self, token: str) -> UUID | None:
        """Returns a user id from token"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://auth.service:8000/api/v1/auth/certs"
            ) as response:
                data = await response.json()
                algorithm = data["data"]["alg"]
                pub_key = data["data"]["key"]
                try:
                    payload = jwt.decode(
                        token,
                        pub_key,
                        algorithms=[algorithm],
                    )
                    user_id = payload.get("sub")
                    return UUID(user_id)
                except (jwt.DecodeError, ValueError, KeyError):
                    return None
