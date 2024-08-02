import uuid
from dataclasses import dataclass

from src.domain.entities import User
from src.domain.exceptions import UserNotFoundException
from src.domain.services import BaseUserService
from src.gateways.postgresql.dto import UserDto
from src.gateways.postgresql.repositories import BaseUserRepository


@dataclass
class UserService(BaseUserService):
    user_repository: BaseUserRepository

    async def update(self, id: uuid.UUID, user: User) -> None:
        await self.get_by_id(id)
        dto = UserDto.from_entity(user)
        dto.id = id
        await self.user_repository.update(dto)
        return None

    async def delete(self, id: uuid.UUID) -> None:
        await self.get_by_id(id)
        await self.user_repository.delete(id)
        return None

    async def get_by_id(self, id: uuid.UUID) -> User:
        dto = await self.user_repository.get_by_id(id)
        if not dto:
            raise UserNotFoundException
        return dto.to_entity()

    async def find_many(
        self, offset: int, limit: int, search: str | None = None
    ) -> list[User]:
        dto_iter = await self.user_repository.find_many(
            offset=offset, limit=limit, search=search
        )
        return [dto.to_entity() for dto in dto_iter]

    async def count_many(self, search: str | None = None) -> int:
        return await self.user_repository.count_many(search=search)
