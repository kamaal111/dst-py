from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8)
