import uuid
from dataclasses import dataclass

from src.api.v1.schemas import ListPaginatedResponse, PaginationOutSchema, UserOut
from src.application.commands.user import (
    AddFriendCommand,
    DeleteFriendCommand,
    GetUserFriendsListCommand,
    GetUsersListCommand,
)
from src.domain.exceptions.friends import AlreadyFriendsException
from src.domain.users.entities import Friends
from src.domain.users.service import BaseFriendsService, BaseUserService
from src.gateways.postgresql.transaction import BaseTransactionManager


@dataclass
class DeleteFriendUseCase:
    user_service: BaseUserService
    friends_service: BaseFriendsService

    transaction_manager: BaseTransactionManager

    async def execute(self, user_id: uuid.UUID, friend_id: uuid.UUID) -> None:
        await self.user_service.get_by_id(id=user_id)
        friends = await self.friends_service.get_by_user_and_friend_id(
            user_id=user_id, friend_id=friend_id
        )
        await self.friends_service.delete(id=friends.id)
        await self.transaction_manager.commit()
        return
