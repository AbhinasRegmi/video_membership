from fastapi import HTTPException, status


class TokenInvalidError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Login to gain valid tokens."
        )