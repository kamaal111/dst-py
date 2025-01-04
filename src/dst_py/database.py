from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///database.db"


class Database:
    engine: "Engine"

    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, echo=False)

    def create_db_and_tables(self):
        from dst_py.models import User  # noqa: F401

        SQLModel.metadata.create_all(self.engine)
