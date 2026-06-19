def test_ping(client):
    res = client.get("/api/v1/ping")
    assert res.status_code == 200
    assert res.json() == {"message": "pong"}


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "environment" in data
