from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class StandardResponse(BaseModel):
    details: str


class UserSchema(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8)


class AccessToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class LoginResponse(StandardResponse, AccessToken):
    random: float
    external_data: list[dict]


class RegisterResponse(StandardResponse): ...
