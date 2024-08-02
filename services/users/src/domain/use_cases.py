import uuid
from dataclasses import dataclass

from src.api.v1.schemas import ListPaginatedResponse, PaginationOutSchema, UserOut
from src.domain.commands import GetUsersListCommand
from src.gateways.postgresql.repositories import BaseUserRepository
from src.services.user import UserService


@dataclass
class GetUsersListUseCase:
    user_repository: BaseUserRepository

    async def execute(
        self, command: GetUsersListCommand
    ) -> ListPaginatedResponse[UserOut]:
        users = await self.user_repository.find_many(
            limit=command.pagiantion.limit,
            offset=command.pagiantion.offset,
            search=command.search,
        )
        count = await self.user_repository.count_many()
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
    user_service: UserService

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
