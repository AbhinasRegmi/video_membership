from fastapi import HTTPException, status

class InvalidYoutubeUrlError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot parse youtube url provided."
        )
    

class VideoAlreadyExistError(HTTPException):
    def __init__(self) -> None:
        return super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Video with given url already exists."
        )