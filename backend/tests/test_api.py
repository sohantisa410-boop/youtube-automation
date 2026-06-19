from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_unauthorized_access(client: TestClient):
    response = client.get("/api/v1/channels")
    assert response.status_code == 401


def test_register_and_duplicate_signup(client: TestClient):
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "strongpass",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 200
    assert first.json()["email"] == payload["email"]

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already registered"


def test_login_with_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_validation_error_returns_422(client: TestClient):
    response = client.post("/api/v1/auth/register", json={"email": "notanemail"})
    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
