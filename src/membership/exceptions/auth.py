from fastapi import status, HTTPException


class NoAuthHeadersError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Authentication Headers found."
        )
    
class UserNotRegisteredError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The user has not been registered yet. Try again later."
        )
    
class NoAcessTokenCookieError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No AccessToken found in Cookies."
        )