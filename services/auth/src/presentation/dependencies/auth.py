from typing import Annotated, Dict, Optional

from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from src.domain.exceptions.user import UserIsNotAuthorizedException


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(
            password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes)
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str | None = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise UserIsNotAuthorizedException
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie("/api/v1/auth/login")


async def auth_required(
    request: Request,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> None:
    if not token:
        raise UserIsNotAuthorizedException

    request.scope["auth"] = token
