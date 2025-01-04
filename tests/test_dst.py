import random
from datetime import datetime

import responses
from freezegun import freeze_time

USER = {
    "address": {
        "city": "Lebsackbury",
        "geo": {"lat": "-38.2386", "lng": "57.2232"},
        "street": "Kattie Turnpike",
        "suite": "Suite 198",
        "zipcode": "31428-2261",
    },
    "company": {
        "bs": "target end-to-end models",
        "catchPhrase": "Centralized empowering task-force",
        "name": "Hoeger LLC",
    },
    "email": "Rey.Padberg@karina.biz",
    "id": 10,
    "name": "Clementina DuBuque",
    "phone": "024-648-3804",
    "username": "Moriah.Stanton",
    "website": "ambrose.net",
}


@responses.activate
@freeze_time("2025-01-01 00:00:00")
def test_read_users_endpoint(client):
    # Double checking that freeze time has been set up correctly
    assert datetime.now() == datetime(2025, 1, 1)

    responses.add(
        responses.GET,
        "https://jsonplaceholder.typicode.com/users",
        json=[USER],
        status=200,
    )

    random.seed(12345)

    users_response = client.get("/auth/users")

    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url == "https://jsonplaceholder.typicode.com/users"
    )
    assert users_response.status_code == 200

    json_response = users_response.json()

    assert isinstance(json_response, dict)
    assert len(json_response["users"]) == 1
    assert json_response["users"][0] == USER
    assert json_response["time"] == "2025-01-01T00:00:00+00:00"
    assert json_response["random"] == 0.41661987254534116
    assert json_response["status"] == 200


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"message": "PONG"}
