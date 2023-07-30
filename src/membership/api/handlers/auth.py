from pydantic import EmailStr, ValidationError
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from membership.core.template import htemplate
from membership.core.path import MembershipPath

from membership.schemas.token import JWTTokenData
from membership.schemas.user import UserSigninSchema

from membership.models.user import UserModel
from membership.utils.jwt import generate_jwt_access_token
from membership.exceptions.user import UserAlreadyExistError

auth_handler = APIRouter()


@auth_handler.get("/user/signup", response_class=HTMLResponse)
def user_get_signup(request: Request):
    context = {
        "request": request
    }

    return htemplate.TemplateResponse("/signup.html", context=context)

#  response_class=Union[HTMLResponse, RedirectResponse]
@auth_handler.post(
        "/user/signup",
        responses={
            status.HTTP_303_SEE_OTHER: {
                "description": "Redirects to home page on successfull account creation.",
            },
            status.HTTP_200_OK: {
                "description": "Try again on failed account creation."
            }
        })
def user_post_signup(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...)
):
    errors = []

    try:
        
        UserSigninSchema(
            email=email, 
            password=password, 
            password_confirm=password_confirm)
        
        UserModel.create_user(
            email=email,
            password=password
        )

        return RedirectResponse(url=MembershipPath.LOGIN_URL, status_code=status.HTTP_303_SEE_OTHER)
        
    except ValidationError as e:
        for error in e.errors():
            errors.append(error['msg'])
            
    except UserAlreadyExistError as e:
        errors.append(e.detail)

    context = {
        "request": request,
        "data": {"email": email},
        "errors": errors
    }

    return htemplate.TemplateResponse("/signup.html", context=context)


@auth_handler.get("/user/login", response_class=HTMLResponse)
def login_view(request: Request):
    context = {
        "request": request
    }

    return htemplate.TemplateResponse("/login.html", context=context)

# response_class=Union[HTMLResponse, RedirectResponse]
@auth_handler.post("/user/login")
def login_post_view(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    errors = []

    try:
        # UserLoginSchema(email=email, password=password)

        if not (user:=UserModel.get_user_with_validation(email=email, password=password)):
            raise ValueError("Incorrect email or password.")
        
        token_data = JWTTokenData(sub=email)
        access_token = generate_jwt_access_token(token_data)

        response = RedirectResponse(url=MembershipPath.HOME_PAGE_URL, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token)

        return response
    
    except ValueError as e:
        errors.append(e)

    context = {
        "request": request,
        "data": {"email": email},
        "errors": errors
    }

    return htemplate.TemplateResponse('/login.html', context=context)


@auth_handler.get("/user/logout", response_class=RedirectResponse)
def logout_user(request: Request):
    context = {
        "request": request
    }

    response = RedirectResponse(url=MembershipPath.LOGIN_URL)
    
    for key in request.cookies.keys():
        if key == "access_token":
            response.delete_cookie(key=key)
    
    return response