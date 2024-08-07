import uuid
from dataclasses import dataclass

from src.api.v1.schemas import ListPaginatedResponse, PaginationOutSchema, UserOut
from src.application.commands.user import (
    AddFriendCommand,
    GetUserFriendsListCommand,
    GetUsersListCommand,
)
from src.domain.exceptions.friends import AlreadyFriendsException
from src.domain.users.entities import Friends
from src.domain.users.service import BaseFriendsService, BaseUserService
from src.gateways.postgresql.transaction import BaseTransactionManager


@dataclass
class AddFriendUseCase:
    user_service: BaseUserService
    friends_service: BaseFriendsService

    transaction_manager: BaseTransactionManager

    async def execute(self, user_id: uuid.UUID, command: AddFriendCommand) -> None:
        await self.user_service.get_by_id(id=user_id)
        friends = Friends.create(user_id=user_id, friend_id=command.friend_id)
        await self.friends_service.create(friends=friends)
        await self.transaction_manager.commit()
        return


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
