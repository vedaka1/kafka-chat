from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.application.contracts.commands.user import *
from src.application.contracts.common.response import APIResponse
from src.application.contracts.responses.user import UserOut
from src.application.usecases.auth import *
from src.application.usecases.auth.login import LoginUseCase
from src.domain.users.user import User

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
    route_class=DishkaRoute,
)


@router.post("/register", summary="Creates a new user")
async def register(
    command: RegisterCommand,
    register_user_interactor: FromDishka[RegisterUseCase],
) -> APIResponse:
    await register_user_interactor.execute(command)
    return APIResponse(ok=True)


@router.post("/login", summary="Authenticate user")
async def login(
    login_interactor: FromDishka[LoginUseCase],
    command: LoginCommand,
    response: Response,
    # credentials: OAuth2PasswordRequestForm = Depends(),
) -> APIResponse[UserOut]:
    # user, token = await login_interactor.execute(
    #     LoginCommand(password=credentials.password, email=credentials.username)
    # )
    user, token = await login_interactor.execute(command)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=token.max_age,
        httponly=True,
    )
    return APIResponse(ok=True, data=user)
