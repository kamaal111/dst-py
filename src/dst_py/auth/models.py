from __future__ import annotations

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    __tablename__: str = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=8)

    @staticmethod
    def create(email: str, raw_password: str, session: Session | None) -> User:
        hashed_password = pwd_context.hash(raw_password)
        user = User(email=email, password=hashed_password)
        if session:
            session.add(user)

        return user
