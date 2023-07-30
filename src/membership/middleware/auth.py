"""
Auth middleware that adds user to request.
"""

from fastapi import status
from fastapi.responses import RedirectResponse

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


from membership.core.path import MembershipPath
from membership.core.template import htemplate
from membership.utils.jwt import validate_access_token
from membership.exceptions.token import TokenInvalidError

class UserAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            access_token = request.cookies.get('access_token')

            if not access_token:
                request.state.is_authenticated = False
            elif token_data:= validate_access_token(access_token):
                request.state.is_authenticated = True
                request.state.user_email = token_data.sub
            else:
                request.state.is_authenticated = False

            response = await call_next(request)
            return response
        
        except TokenInvalidError:
            request.state.is_authenticated = False
            response = await call_next(request)
            return response