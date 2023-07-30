"""
Handling for Authentication Header Not found.
"""
from fastapi import Request, status
from fastapi.responses import RedirectResponse

from membership.core.path import MembershipPath
from membership.exceptions.auth import NoAuthHeadersError


async def auth_header_exc_handler(request: Request, exc: NoAuthHeadersError):
    return RedirectResponse(
        url=MembershipPath.LOGIN_URL,
        status_code=status.HTTP_303_SEE_OTHER
    )