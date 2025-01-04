from __future__ import annotations

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Session, select

from .exceptions import UserAlreadyExists
from .schemas import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    __tablename__: str = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    password: str

    def verify_password(self, raw_password: str) -> bool:
        return pwd_context.verify(raw_password, self.password)

    @staticmethod
    def get_by_email(email: str, session: Session) -> User | None:
        query = select(User).where(User.email == email).limit(1)

        return session.exec(query).first()

    @classmethod
    def create(cls, payload: UserSchema, session: Session, commit=True) -> User:
        existing_user = User.get_by_email(email=payload.email, session=session)
        if existing_user is not None:
            raise UserAlreadyExists()

        hashed_password = pwd_context.hash(payload.password)
        user = User(email=payload.email, password=hashed_password)

        session.add(user)
        if commit:
            session.commit()

        return user
