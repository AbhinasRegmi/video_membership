"""
All jwt token generation and validation.
"""
from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import ValidationError

from membership.core.config import settings
from membership.schemas.token import JWTTokenData
from membership.exceptions.token import TokenInvalidError

def generate_jwt_access_token(data: JWTTokenData) -> str:
    to_encode = dict(data).copy()
    to_encode.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXP)
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.MEMBERSHIP_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def validate_access_token(access_token: str) -> JWTTokenData:
    try:
        payload = jwt.decode(
            access_token,
            settings.MEMBERSHIP_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return JWTTokenData(**payload)
    except (ValidationError, JWTError):
        raise TokenInvalidError
    