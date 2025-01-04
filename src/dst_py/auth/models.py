from __future__ import annotations

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Session, select

from .exceptions import UserAlreadyExists

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    __tablename__: str = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    password: str

    @staticmethod
    def create(email: str, raw_password: str, session: Session, commit=True) -> User:
        existing_user_query = select(User).where(User.email == email).limit(1)
        existing_user = session.exec(existing_user_query).first()
        if existing_user is not None:
            raise UserAlreadyExists()

        hashed_password = pwd_context.hash(raw_password)
        user = User(email=email, password=hashed_password)

        session.add(user)
        if commit:
            session.commit()

        return user
