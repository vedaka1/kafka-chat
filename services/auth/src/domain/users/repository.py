import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.users.user import User, UserConfirmation


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def update(self, user_id: uuid.UUID, user: User) -> None: ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def _get_by(self, value: uuid.UUID | str, filter: str) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[User]: ...

    @abstractmethod
    async def count(self) -> int | None: ...


@dataclass
class BaseUserConfirmationRepository(ABC):
    @abstractmethod
    async def create(self, user_confirmation: UserConfirmation) -> None: ...

    @abstractmethod
    async def update(
        self, confirmation_id: uuid.UUID, user_confirmation: UserConfirmation
    ) -> None: ...

    @abstractmethod
    async def delete(self, confirmation_id: uuid.UUID) -> None: ...

    @abstractmethod
    async def get_by_id(
        self, confirmation_id: uuid.UUID
    ) -> UserConfirmation | None: ...
