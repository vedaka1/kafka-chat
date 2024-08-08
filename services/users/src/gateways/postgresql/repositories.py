import uuid

from sqlalchemy import delete, func, insert, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.users.repository import BaseFriendsRepository, BaseUserRepository
from src.gateways.postgresql.dto import FriendsDto, UserDto
from src.gateways.postgresql.models import FriendsModel, UserModel


class UserRepository(BaseUserRepository):
    session: AsyncSession

    async def create(self, user: UserDto) -> UserDto:
        query = insert(UserModel).values(user.dump())
        await self.session.execute(query)
        return user

    async def delete(self, id: uuid.UUID) -> None:
        query = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(query)
        return None

    async def update(self, user: UserDto) -> None:
        query = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(username=user.username)
        )
        await self.session.execute(query)
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


class FriendsRepository(BaseFriendsRepository):
    session: AsyncSession

    async def create(self, friends: FriendsDto) -> None:
        query = insert(FriendsModel).values(
            {
                "user_id": friends.user_id,
                "friend_id": friends.friend_id,
                "created_at": friends.created_at,
            }
        )
        await self.session.execute(query)
        return None

    async def delete(self, id: int) -> None:
        query = delete(FriendsModel).where(FriendsModel.id == id)
        await self.session.execute(query)
        return None

    async def update(self, friends: FriendsDto) -> None:
        query = update(FriendsModel).where(FriendsModel.id == id).values(friends.dump())
        await self.session.execute(query)
        return None

    async def get_by_id(self, id: int) -> FriendsDto | None:
        query = select(FriendsModel).where(FriendsModel.id == id)
        result = await self.session.execute(query)
        friends = result.scalar_one_or_none()
        return FriendsDto.from_entity(friends) if friends else None

    async def get_by_user_id(
        self, user_id: uuid.UUID, offset: int, limit: int
    ) -> list[FriendsDto]:
        query = (
            select(FriendsModel)
            .where(FriendsModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        data = result.scalars().all()
        return [FriendsDto.from_entity(item) for item in data]

    async def get_friends_by_user_id(
        self, user_id: uuid.UUID, offset: int, limit: int
    ) -> list[UserDto]:
        query = (
            select(UserModel)
            .select_from(FriendsModel)
            .join(UserModel, FriendsModel.user_id == UserModel.id)
            .where(FriendsModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        data = result.scalars().all()
        return [UserDto.from_entity(item) for item in data]

    async def get_all(self, limit: int = 10, offset: int = 0) -> list[FriendsDto]:
        query = select(FriendsModel).limit(limit).offset(offset)
        result = await self.session.execute(query)
        data = result.scalars().all()
        return [FriendsDto.from_entity(item) for item in data]

    async def count_many(self, user_id: uuid.UUID) -> int:
        query = (
            select(func.count())
            .select_from(FriendsModel)
            .where(FriendsModel.user_id == user_id)
        )
        result = await self.session.execute(query)
        count = result.scalars().one_or_none()
        return count if count else 0

    async def get_by_user_and_friend_id(
        self, user_id: uuid.UUID, friend_id: uuid.UUID
    ) -> FriendsDto | None:
        query = (
            select(FriendsModel)
            .where(FriendsModel.user_id == user_id)
            .where(FriendsModel.friend_id == friend_id)
        )
        result = await self.session.execute(query)
        friends = result.scalar_one_or_none()
        return FriendsDto.from_entity(friends) if friends else None
