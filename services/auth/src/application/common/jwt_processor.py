import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseJwtTokenProcessor(ABC):
    @abstractmethod
    def generate_token(self, user_id: uuid.UUID) -> str: ...

    @abstractmethod
    def validate_token(self, token: str) -> uuid.UUID | None: ...
