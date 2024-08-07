import uuid
from dataclasses import dataclass

from src.domain.exceptions.friends import (
    AlreadyFriendsException,
    FriendNotFoundException,
)
from src.domain.exceptions.user import UserNotFoundException
from src.domain.users.entities import Friends
from src.domain.users.repository import BaseFriendsRepository
from src.domain.users.service import BaseFriendsService
from src.gateways.postgresql.dto import FriendsDto


@dataclass
class FriendsService(BaseFriendsService):
    friends_repository: BaseFriendsRepository

    async def create(self, friends: Friends) -> None:
        friend = await self.friends_repository.get_by_user_and_friend_id(
            user_id=friends.user_id, friend_id=friends.friend_id
        )
        if friend:
            raise AlreadyFriendsException
        dto = FriendsDto.from_entity(friends)
        await self.friends_repository.create(dto)
        return None

    async def update(self, id: int, user: Friends) -> None:
        await self.get_by_id(id)
        dto = FriendsDto.from_entity(user)
        dto.id = id
        await self.friends_repository.update(dto)
        return None

    async def delete(self, id: int) -> None:
        await self.friends_repository.delete(id)
        return None

    async def get_by_id(self, id: int) -> Friends:
        dto = await self.friends_repository.get_by_id(id)
        if not dto:
            raise FriendNotFoundException
        return dto.to_entity()

    async def get_by_user_id(
        self,
        user_id: uuid.UUID,
        offset: int,
        limit: int,
    ) -> list[Friends]:
        dto_iter = await self.friends_repository.get_by_user_id(
            user_id=user_id, offset=offset, limit=limit
        )
        return [dto.to_entity() for dto in dto_iter]

    async def get_by_user_and_friend_id(
        self, user_id: uuid.UUID, friend_id: uuid.UUID
    ) -> Friends | None:
        dto = await self.friends_repository.get_by_user_and_friend_id(
            user_id=user_id, friend_id=friend_id
        )
        if not dto:
            raise FriendNotFoundException
        return dto.to_entity()

    # async def find_many(
    #     self, offset: int, limit: int, search: str | None = None
    # ) -> list[Friends]:
    #     dto_iter = await self.friends_repository.find_many(
    #         offset=offset, limit=limit, search=search
    #     )
    #     return [dto.to_entity() for dto in dto_iter]

    async def count_many(self, user_id: uuid.UUID) -> int:
        return await self.friends_repository.count_many(user_id=user_id)
