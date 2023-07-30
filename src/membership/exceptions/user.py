from fastapi import HTTPException, status


class UserAlreadyExistError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User with this email already exits."
        )