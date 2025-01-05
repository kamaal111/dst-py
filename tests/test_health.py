def test_ping(databaseless_client):
    response = databaseless_client.get("/health/ping")

    assert response.status_code == 200
    assert response.json() == {"message": "PONG"}
