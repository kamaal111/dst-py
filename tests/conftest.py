import random
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time
from sqlalchemy import create_engine
from sqlmodel import Session, select

from dst_py.auth.models import User
from dst_py.auth.schemas import UserSchema
from dst_py.database import BaseDatabase, get_database
from dst_py.main import app


class DatabaseForTests(BaseDatabase):
    def __init__(self, database_name: str) -> None:
        super().__init__(
            create_engine(
                database_name, connect_args={"check_same_thread": False}, echo=False
            )
        )


def get_database_override(database: DatabaseForTests):
    def override():
        yield database

    return override


def get_databaseless_override():
    yield None


@pytest.fixture
def database():
    temporary_directory = __get_or_create_temporary_directory_if_not_exists()
    database_path = temporary_directory / f"{uuid.uuid4()}.db"
    database = DatabaseForTests(f"sqlite:///{database_path}")
    database.create_db_and_tables()

    try:
        yield database
    finally:
        database_path.unlink()


@pytest.fixture(scope="function")
def client(database, create_default_user):
    __client = TestClient(app)
    app.dependency_overrides[get_database] = get_database_override(database)

    try:
        yield __client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def databaseless_client():
    __client = TestClient(app)
    app.dependency_overrides[get_database] = get_databaseless_override

    try:
        yield __client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def default_user_credentials():
    yield UserSchema(email="yami@bulls.io", password="nice_password")


@pytest.fixture
def create_default_user(database, default_user_credentials):
    with Session(database.engine) as session:
        query = select(User).where(User.email == default_user_credentials.email)
        if user := session.exec(query).first():
            yield user

        yield User.create(payload=default_user_credentials, session=session)


@pytest.fixture
def freeze_test_time():
    with freeze_time("2025-01-01 10:00:00"):
        yield


@pytest.fixture
def deterministic_random():
    random.seed(12345)
    yield


def __get_or_create_temporary_directory_if_not_exists():
    temporary_directory = Path("tmp")
    temporary_directory.mkdir(parents=True, exist_ok=True)

    return temporary_directory
