from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from dst_py.settings import settings


class Database:
    engine: "Engine"

    def __init__(self) -> None:
        self.engine = create_engine(settings.database_url, echo=False)

    def create_db_and_tables(self):
        from dst_py.auth.models import User  # noqa: F401

        SQLModel.metadata.create_all(self.engine)
