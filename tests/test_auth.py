from http import HTTPStatus

import responses
from sqlmodel import Session

from dst_py.auth.models import User

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
def test_deterministic_login(
    client, freeze_test_time, deterministic_random, default_user_credentials
):
    responses.add(
        responses.GET,
        "https://jsonplaceholder.typicode.com/users",
        json=[USER],
        status=200,
    )

    login_payload = {
        **default_user_credentials.model_dump(mode="python"),
        "password": "can_be_anything_wrong",
    }
    login_response = client.post("/auth/login", data=login_payload)

    assert login_response.status_code == HTTPStatus.UNAUTHORIZED

    login_payload["password"] = default_user_credentials.password
    login_response = client.post("/auth/login", data=login_payload)
    json_response = login_response.json()

    assert login_response.status_code == HTTPStatus.OK
    assert len(json_response["external_data"]) == 1
    assert json_response["external_data"][0] == USER
    assert json_response["random"] == 0.41661987254534116
    assert json_response["token_type"] == "bearer"
    assert (
        json_response["access_token"]
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTczNTcyNzQwMH0.WB-Skcc2-Qjtmun2SftTdCeSpGmpZOHmXGfeAvapidA"
    )


@responses.activate
def test_deterministic_register(
    client, database, freeze_test_time, deterministic_random
):
    responses.add(
        responses.GET,
        "https://jsonplaceholder.typicode.com/users",
        json=[USER],
        status=200,
    )

    payload = {"email": "yuno@golden.io", "password": "password-to-keep"}
    register_response = client.post("/auth/register", data=payload)
    json_response = register_response.json()

    assert register_response.status_code == HTTPStatus.CREATED
    assert json_response["details"] == "Created"

    with Session(database.engine) as session:
        user = User.get_by_email(email=payload["email"], session=session)

        assert user is not None
        assert user.email == payload["email"]
        assert user.verify_password(raw_password=payload["password"])

    login_response = client.post("/auth/login", data=payload)
    json_response = login_response.json()

    assert login_response.status_code == HTTPStatus.OK
    assert json_response["random"] == 0.41661987254534116
    assert json_response["token_type"] == "bearer"
    assert (
        json_response["access_token"]
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsImV4cCI6MTczNTcyNzQwMH0.Jku3-3o_7x_pLSUrIxMwODMjhPb2DJWtop1RtW3JsYc"
    )
