from __future__ import annotations

import bcrypt
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Session, select

from .exceptions import UserAlreadyExists
from .schemas import UserSchema

PASSWORD_HASHING_ENCODING = "utf-8"


class User(SQLModel, table=True):
    __tablename__: str = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    password: bytes

    def verify_password(self, raw_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode(PASSWORD_HASHING_ENCODING),
            self.password,
        )

    @staticmethod
    def get_by_email(email: str, session: Session) -> User | None:
        query = select(User).where(User.email == email).limit(1)

        return session.exec(query).first()

    @classmethod
    def create(cls, payload: UserSchema, session: Session, commit=True) -> User:
        existing_user = User.get_by_email(email=payload.email, session=session)
        if existing_user is not None:
            raise UserAlreadyExists()

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(
            payload.password.encode(PASSWORD_HASHING_ENCODING), salt
        )
        user = User(
            email=payload.email,
            password=hashed_password,
        )

        session.add(user)
        if commit:
            session.commit()

        return user
