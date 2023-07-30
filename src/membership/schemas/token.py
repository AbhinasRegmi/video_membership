from pydantic import BaseModel, EmailStr


class JWTTokenData(BaseModel):
    sub: EmailStr