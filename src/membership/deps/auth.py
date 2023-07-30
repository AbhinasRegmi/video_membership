from typing import Optional

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import APIKeyCookie

from membership.models.user import UserModel
from membership.schemas.token import JWTTokenData
from membership.utils.jwt import validate_access_token
from membership.exceptions.auth import NoAuthHeadersError, UserNotRegisteredError, NoAcessTokenCookieError

class AccessTokenBearer(HTTPBearer):
    def __init__(self, *args, **kwargs):
        super().__init__(auto_error=False, *args, **kwargs)

    async def __call__(self, request: Request) -> str:
        """
        Only return the auth_token leave out the scheme
        """
        http_auth_credentials: Optional[HTTPAuthorizationCredentials]  = await super().__call__(request)

        if not http_auth_credentials:
            raise NoAuthHeadersError
        
        return http_auth_credentials.credentials
    

class CookieBearer(APIKeyCookie):
    def __init__(self, *args, **kwargs):
        super().__init__(name="access_token", auto_error=False, *args, **kwargs)


    async def __call__(self, request: Request) -> str:
        """
        Only return the access_token from cookies
        """
        access_token = request.cookies.get("access_token")

        if not access_token: #type:ignore
            raise NoAcessTokenCookieError

        return access_token #type:ignore


t_oauth2_scheme = AccessTokenBearer(
    scheme_name="access_token",
    description="Login to gain access_token."
)

c_oauth2_scheme = CookieBearer(
    scheme_name="access_token",
    description="Login to gain access_token."
)

def t_login_required(token: str = Depends(t_oauth2_scheme)) -> JWTTokenData:
    return validate_access_token(token)

def c_login_required(token: str = Depends(c_oauth2_scheme)) -> JWTTokenData:
    return validate_access_token(token)


def t_get_curr_user(token_data: JWTTokenData = Depends(t_login_required)) -> UserModel:
    """
    The sub of token sent should be email of the user for this to work.
    """
    if not (user:=UserModel.get_user_by_email(email=token_data.sub)):
        raise UserNotRegisteredError

    return user


def c_get_curr_user(token_data: JWTTokenData = Depends(c_login_required)) -> UserModel:
    """
    The sub of token sent should be email of the user for this to work.
    """
    if not (user:=UserModel.get_user_by_email(email=token_data.sub)):
        raise UserNotRegisteredError

    return user