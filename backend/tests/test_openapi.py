from fastapi.testclient import TestClient


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "/api/v1/auth/login" in schema["paths"]
    assert "/api/v1/auth/register" in schema["paths"]
    assert "/api/v1/channels" in schema["paths"]
    assert schema["openapi"] in {"3.0.0", "3.1.0"}
    assert schema["info"]["title"] == "YouTube Automation System"
