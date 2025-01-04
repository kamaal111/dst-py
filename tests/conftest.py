import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from dst_py.database import BaseDatabase, get_database
from dst_py.main import app


class DatabaseForTests(BaseDatabase):
    def __init__(self, database_name: str) -> None:
        super().__init__(create_engine(database_name, echo=False))


def get_database_override(database_name: str):
    database = DatabaseForTests(database_name)
    database.create_db_and_tables()

    def override():
        yield database

    return override


@pytest.fixture(scope="function")
def client():
    __client = TestClient(app)
    database_filename = f"{uuid.uuid4()}.db"
    database_name = f"sqlite:///{database_filename}"
    app.dependency_overrides[get_database] = get_database_override(database_name)

    try:
        yield __client
    finally:
        Path(database_filename).unlink()
