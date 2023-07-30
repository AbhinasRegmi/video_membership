from fastapi import Depends, Form
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from membership.core.template import htemplate
from membership.core.path import MembershipPath
from membership.models.video import VideoModel
from membership.deps.auth import c_get_curr_user
from membership.exceptions.video import VideoAlreadyExistError, InvalidYoutubeUrlError

video_handler = APIRouter(
    prefix="/video"
)


@video_handler.get("/upload", response_class=HTMLResponse)
def upload_video_get(
    request: Request,
    user = Depends(c_get_curr_user)
    ):
    context = {
        "request": request
    }

    return htemplate.TemplateResponse('/video_upload.html', context=context)

@video_handler.post("/upload")
def upload_video_post(
    request: Request,
    user = Depends(c_get_curr_user),
    url: str = Form(...)):

    try:
        VideoModel.create_video(
            youtube_url=url,
            user=user
        )

        return RedirectResponse(
            url=MembershipPath.VIDEO_URL,
            status_code=status.HTTP_303_SEE_OTHER)
    
    except (InvalidYoutubeUrlError, VideoAlreadyExistError) as e:
        context = {
            "request": request,
            "errors": [].append(e.detail)
        }

        return htemplate.TemplateResponse(
            "/video_upload.html",
            context=context
        )
    

@video_handler.get("/", response_class=HTMLResponse)
def video_collection_get(request: Request):
    context = {
        "request": request
    }

    return htemplate.TemplateResponse(
        "/video.html",
        context=context
    )