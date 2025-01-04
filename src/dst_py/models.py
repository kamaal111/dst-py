from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__: str = "user"
    __table_args__ = (UniqueConstraint("email"),)

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    password: str
