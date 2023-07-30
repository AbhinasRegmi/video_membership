from dataclasses import dataclass

@dataclass(frozen=True)
class MembershipPath:
    HOME_PAGE_URL: str = "/"
    LOGIN_URL: str = "/user/login"
    SIGNUP_URL: str = "/user/signup"
    VIDEO_URL: str = "/video"
    VIDEO_UPLOAD: str = "/video/upload"


