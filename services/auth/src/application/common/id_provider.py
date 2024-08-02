import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseIdProvider(ABC):
    @abstractmethod
    def get_current_user_id(self, *, token: str) -> uuid.UUID: ...
