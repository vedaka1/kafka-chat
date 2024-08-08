from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.api.v1.schemas import (
    APIResponse,
    ListPaginatedResponse,
    PaginationQuery,
    UserOut,
)
from src.application.commands.user import AddFriendCommand, GetUserFriendsListCommand
from src.application.usecases.create import AddFriendUseCase
from src.application.usecases.delete import DeleteFriendUseCase
from src.application.usecases.get import GetUserFriendsListUseCase
from src.utils.dependencies import get_current_user_id

router = APIRouter(
    prefix="/users",
    tags=["Users friends"],
    route_class=DishkaRoute,
)


def get_pagination(limit=10, offset=0) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)


def get_user_friends_list_command(
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUserFriendsListCommand:
    return GetUserFriendsListCommand(pagination=pagination)


@router.get(
    "/me/friends",
    summary="Get user friends list",
)
async def get_user_friends_list(
    get_friends_interactor: FromDishka[GetUserFriendsListUseCase],
    user_id: UUID = Depends(get_current_user_id),
    command: GetUserFriendsListCommand = Depends(get_user_friends_list_command),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_friends_interactor.execute(user_id=user_id, command=command)
    return APIResponse(ok=True, data=response)


@router.post(
    "/me/friends",
    summary="Add friend",
)
async def add_friend(
    add_friend_interactor: FromDishka[AddFriendUseCase],
    command: AddFriendCommand = Depends(),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse:
    response = await add_friend_interactor.execute(user_id=user_id, command=command)
    return APIResponse(ok=True, data=response)


@router.delete(
    "/me/friends/{friend_id}",
    summary="Delete friend",
)
async def add_friend(
    delete_friend_interactor: FromDishka[DeleteFriendUseCase],
    friend_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse:
    response = await delete_friend_interactor.execute(
        user_id=user_id, friend_id=friend_id
    )
    return APIResponse(ok=True, data=response)
