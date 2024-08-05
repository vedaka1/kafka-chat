import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.gateways.postgresql.dto import UserDto
from src.gateways.postgresql.models import UserModel


@dataclass
class BaseUserRepository(ABC):
    session: AsyncSession

    @abstractmethod
    async def create(self, user: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def delete(self, id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def update(self, user: UserDto) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: uuid.UUID) -> UserDto | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDto]:
        pass

    @abstractmethod
    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[UserDto]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass


class UserRepository(BaseUserRepository):
    async def create(self, user: UserDto) -> UserDto:
        query = insert(UserModel).values(user.dump())
        await self.session.execute(query)
        await self.session.commit()
        return user

    async def delete(self, id: uuid.UUID) -> None:
        query = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(query)
        await self.session.commit()
        return None

    async def update(self, user: UserDto) -> None:
        query = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(username=user.username)
        )
        await self.session.execute(query)
        await self.session.commit()
        return None

    async def get_by_id(self, id: uuid.UUID) -> UserDto | None:
        query = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return UserDto.from_entity(user) if user else None

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[UserDto]:
        query = select(UserModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        data = result.scalars().all()
        return [UserDto.from_entity(item) for item in data]

    async def find_many(
        self,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None,
    ) -> list[UserDto]:
        if search:
            query = (
                select(UserModel)
                .where(
                    UserModel.username.ilike(
                        "%{0}%".format(r"%%".join(search.lower().split()))
                    )
                )
                .limit(limit)
                .offset(offset)
            )
        else:
            query = select(UserModel).limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [UserDto.from_entity(user) for user in result.scalars().all()]

    async def count_many(self, search: str | None = None) -> int:
        if search:
            query = (
                select(func.count())
                .select_from(UserModel)
                .where(
                    UserModel.username.ilike(
                        "%{0}%".format(r"%%".join(search.lower().split()))
                    )
                )
            )
        else:
            query = select(func.count()).select_from(UserModel)
        result = await self.session.execute(query)
        count = result.scalars().one_or_none()
        if not count:
            return 0
        return count
