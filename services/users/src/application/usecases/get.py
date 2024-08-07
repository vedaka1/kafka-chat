import uuid
from dataclasses import dataclass

from src.api.v1.schemas import (
    FriendOut,
    ListPaginatedResponse,
    PaginationOutSchema,
    UserOut,
)
from src.application.commands.user import GetUserFriendsListCommand, GetUsersListCommand
from src.domain.users.entities import Friends
from src.domain.users.service import BaseFriendsService, BaseUserService


@dataclass
class GetUsersListUseCase:
    user_service: BaseUserService

    async def execute(
        self, command: GetUsersListCommand
    ) -> ListPaginatedResponse[UserOut]:

        users = await self.user_service.find_many(
            limit=command.pagiantion.limit,
            offset=command.pagiantion.offset,
            search=command.search,
        )
        count = await self.user_service.count_many(search=command.search)
        return ListPaginatedResponse(
            items=[
                UserOut(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    is_superuser=user.is_superuser,
                )
                for user in users
            ],
            pagination=PaginationOutSchema(
                limit=command.pagiantion.limit,
                offset=command.pagiantion.offset,
                total=count,
            ),
        )


@dataclass
class GetUserUseCase:
    user_service: BaseUserService

    async def execute(self, user_id: uuid.UUID) -> UserOut:
        user = await self.user_service.get_by_id(id=user_id)
        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            is_superuser=user.is_superuser,
        )


@dataclass
class GetUserFriendsListUseCase:
    user_service: BaseUserService
    friends_service: BaseFriendsService

    async def execute(
        self, user_id: uuid.UUID, command: GetUserFriendsListCommand
    ) -> ListPaginatedResponse[FriendOut]:
        await self.user_service.get_by_id(id=user_id)
        friends = await self.friends_service.get_by_user_id(
            user_id=user_id,
            limit=command.pagiantion.limit,
            offset=command.pagiantion.offset,
        )
        count = await self.friends_service.count_many(user_id=user_id)
        return ListPaginatedResponse(
            items=[
                FriendOut(
                    id=friend.id,
                    friend_id=friend.friend_id,
                    created_at=friend.created_at,
                )
                for friend in friends
            ],
            pagination=PaginationOutSchema(
                limit=command.pagiantion.limit,
                offset=command.pagiantion.offset,
                total=count,
            ),
        )
