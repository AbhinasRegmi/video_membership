from fastapi import APIRouter

from membership.api.handlers.auth import auth_handler
from membership.api.handlers.home import home_handler
from membership.api.handlers.video import video_handler


template_router = APIRouter()

template_router.include_router(home_handler, tags=["general"])
template_router.include_router(auth_handler, tags=["user"])
template_router.include_router(video_handler, tags=["videos"])