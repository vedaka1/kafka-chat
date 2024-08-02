from dataclasses import dataclass

from src.application.common.id_provider import BaseIdProvider
from src.application.contracts.commands.user import GetUsersListCommand
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationOutSchema,
)
from src.application.contracts.responses.user import UserOut
from src.domain.users.repository import BaseUserRepository


@dataclass
class GetUsersListUseCase:
    user_repository: BaseUserRepository
    id_provider: BaseIdProvider

    async def execute(
        self, command: GetUsersListCommand
    ) -> ListPaginatedResponse[UserOut]:
        id = self.id_provider.get_current_user_id()
        users = await self.user_repository.get_all(
            limit=command.pagiantion.limit,
            offset=command.pagiantion.offset,
        )
        count = await self.user_repository.count()
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