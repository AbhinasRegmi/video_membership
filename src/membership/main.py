from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cassandra.cqlengine.management import sync_table

from membership.core.db import get_cdb
from membership.core.config import settings
from membership.core.template import stemplate

from membership.models.user import UserModel
from membership.models.video import VideoModel

from membership.exceptions.token import TokenInvalidError
from membership.exceptions.auth import NoAuthHeadersError
from membership.exceptions.auth import NoAcessTokenCookieError
from membership.exceptions.handler.auth import auth_header_exc_handler

from membership.middleware.auth import UserAuthMiddleware
from membership.api.router import v1_router, template_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_cdb()
    sync_table(UserModel)
    sync_table(VideoModel)
    yield


app = FastAPI(
    title='Video Membership',
    redoc_url='',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(UserAuthMiddleware)

app.add_exception_handler(NoAuthHeadersError, auth_header_exc_handler)
app.add_exception_handler(NoAcessTokenCookieError, auth_header_exc_handler)
app.add_exception_handler(TokenInvalidError, auth_header_exc_handler)

app.mount("/static", stemplate, name='static')


@app.get('/healthz', tags=['Health'])
async def checkup():
    return {
        "msg": "Welcome to Video Membership Platform."
    }


app.include_router(v1_router)
app.include_router(template_router)