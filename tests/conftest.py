import pytest
from fastapi.testclient import TestClient

from dst_py.main import app

__client = TestClient(app)


@pytest.fixture
def client():
    return __client
