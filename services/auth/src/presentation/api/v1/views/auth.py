from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.application.contracts.commands.user import *
from src.application.contracts.common.cert import Cert, CertsResponse
from src.application.contracts.common.response import APIResponse
from src.application.contracts.responses.user import UserOut
from src.application.usecases.auth import *
from src.infrastructure.config import settings

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
    response: Response,
    login_command: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> APIResponse[UserOut]:
    user, token = await login_interactor.execute(
        LoginCommand(password=login_command.password, username=login_command.username)
    )
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=token.max_age,
        httponly=True,
        secure=True,
    )
    return APIResponse(ok=True, data=user)


@router.post("/logout", summary="Logout")
async def logout(
    response: Response,
) -> APIResponse[UserOut]:
    response.delete_cookie("access_token")
    return APIResponse(ok=True)


@router.get("/certs", summary="A list of public keys to validate JWT Token")
async def certs() -> APIResponse[Cert]:
    return APIResponse(
        ok=True, data=Cert(alg="RS256", kty="RSA", key=settings.jwt.PUBLIC_KEY)
    )


@router.get("/confirmation", summary="Confirms a user")
async def confirmation(
    confirmation_interactor: FromDishka[UserConfirmationUseCase],
    command: UserConfirmationCommand = Depends(),
) -> APIResponse:
    await confirmation_interactor.execute(command)
    return APIResponse(ok=True)
