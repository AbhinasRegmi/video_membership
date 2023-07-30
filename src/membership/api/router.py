from fastapi import APIRouter

from membership.api.handlers.auth import auth_handler
from membership.api.handlers.home import home_handler

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["Auth"]
)

template_router = APIRouter(

)

template_router.include_router(auth_handler)
template_router.include_router(home_handler)