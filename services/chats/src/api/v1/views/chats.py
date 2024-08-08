from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends

from src.api.v1.schemas import APIResponse, ListPaginatedResponse, PaginationQuery
from src.application.commands.chats import CreateChatCommand, GetChatsListCommand
from src.application.usecases.create import CreateChatUseCase
from src.application.usecases.get import GetChatsListUseCase
from src.domain.chats.entities import Chat
from src.utils.dependencies import get_current_user_id

router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    route_class=DishkaRoute,
)


def get_pagination(limit=10, offset=0) -> PaginationQuery:
    return PaginationQuery(offset=offset, limit=limit)


def get_chats_list_command(
    search: str | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetChatsListCommand:
    return GetChatsListCommand(search=search, pagination=pagination)


@router.get("", summary="Get a list of chats")
async def get_chats_list(
    get_chats_interactor: FromDishka[GetChatsListUseCase],
    command: GetChatsListCommand = Depends(get_chats_list_command),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[ListPaginatedResponse[Chat]]:
    result = await get_chats_interactor.execute(command=command)
    return APIResponse(ok=True, data=result)


@router.post("", summary="Create new chat")
async def create_chat(
    create_chat_interactor: FromDishka[CreateChatUseCase],
    command: CreateChatCommand = Depends(),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse:
    await create_chat_interactor.execute(user_id=user_id, command=command)
    return APIResponse(ok=True)
