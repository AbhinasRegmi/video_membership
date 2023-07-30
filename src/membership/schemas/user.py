from pydantic import BaseModel, EmailStr
from pydantic import field_validator, Field, model_validator

class UserResponseSchema(BaseModel):
    email: EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSigninSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    password_confirm: str = Field(..., min_length=6, max_length=16)

    @field_validator('password')
    def validate_secure_password(cls, v: str) -> str:
        if not any(letter.isupper() for letter in v):
            raise ValueError("Password must contain at least one Upper character")
        
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserSigninSchema':
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self