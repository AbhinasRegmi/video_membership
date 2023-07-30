from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends

from membership.core.template import htemplate
from membership.deps.auth import c_login_required


home_handler = APIRouter()


@home_handler.get("/", response_class=HTMLResponse)
def home_view_handler(request: Request):
    context = {
        "request": request
    }

    return htemplate.TemplateResponse("/home.html", context=context)