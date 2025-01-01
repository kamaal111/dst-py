import random
from datetime import datetime

import responses
from freezegun import freeze_time


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"message": "PONG"}


@responses.activate
@freeze_time("2025-01-01 00:00:00")
def test_read_users_endpoint(client):
    # Double checking that freeze time has been set up correctly
    assert datetime.now() == datetime(2025, 1, 1)

    responses.add(
        responses.GET,
        "https://jsonplaceholder.typicode.com/users",
        json=[],
        status=200,
    )

    random.seed(12345)

    response = client.get("/users")

    assert response.json()["users"] == []
