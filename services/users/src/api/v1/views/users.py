from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.api.v1.schemas import (
    APIResponse,
    ListPaginatedResponse,
    PaginationQuery,
    UserOut,
)
from src.application.commands.user import GetUserFriendsListCommand, GetUsersListCommand
from src.application.usecases.get import GetUsersListUseCase, GetUserUseCase
from src.utils.dependencies import get_current_user_id

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
)


def get_pagination(limit=10, offset=0) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)


def get_user_friends_list_command(
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUserFriendsListCommand:
    return GetUserFriendsListCommand(pagination=pagination)


def get_users_list_command(
    search: str | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUsersListCommand:
    return GetUsersListCommand(search=search, pagiantion=pagination)


@router.get(
    "",
    summary="Get users list",
)
async def get_users_list(
    get_users_interactor: FromDishka[GetUsersListUseCase],
    user_id: UUID = Depends(get_current_user_id),
    command: GetUsersListCommand = Depends(get_users_list_command),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_users_interactor.execute(command)
    return APIResponse(ok=True, data=response)


@router.get("/me", summary="Get current user")
async def get_current_user(
    get_user_interactor: FromDishka[GetUserUseCase],
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[UserOut]:
    response = await get_user_interactor.execute(user_id)
    return APIResponse(ok=True, data=response)


@router.get("/{user_id}", summary="Get user by id")
async def get_user_by_id(
    user_id: UUID,
    get_user_interactor: FromDishka[GetUserUseCase],
) -> APIResponse[UserOut]:
    response = await get_user_interactor.execute(user_id)
    return APIResponse(ok=True, data=response)
