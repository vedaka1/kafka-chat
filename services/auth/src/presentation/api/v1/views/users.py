from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.application.contracts.commands.user import *
from src.application.contracts.common.pagination import ListPaginatedResponse
from src.application.contracts.common.response import APIResponse
from src.application.contracts.responses.user import UserOut
from src.application.usecases.auth import *
from src.application.usecases.users.get_user import GetUsersListUseCase
from src.presentation.dependencies.auth import auth_required

router = APIRouter(
    tags=["Users"],
    prefix="/users",
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)],
)


def get_pagination(limit=10, offset=0) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)


def get_users_list_command(
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUsersListCommand:
    return GetUsersListCommand(pagiantion=pagination)


@router.get("", summary="Get a list of users")
async def get_users(
    get_users_interactor: FromDishka[GetUsersListUseCase],
    command: GetUsersListCommand = Depends(get_users_list_command),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_users_interactor.execute(command)
    return APIResponse(ok=True, data=response)
