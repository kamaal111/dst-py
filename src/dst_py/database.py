from typing import Any, Generator

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from dst_py.conf import settings


class BaseDatabase:
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def create_db_and_tables(self):
        from dst_py.auth.models import User  # noqa: F401

        SQLModel.metadata.create_all(self.engine)


class Database(BaseDatabase):
    def __init__(self) -> None:
        super().__init__(create_engine(settings.database_url, echo=True))


database = Database()
database.create_db_and_tables()


def get_database() -> Generator[BaseDatabase, Any, None]:
    yield database
