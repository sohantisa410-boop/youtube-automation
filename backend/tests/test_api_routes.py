from fastapi.testclient import TestClient


def test_ping_route(client: TestClient):
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_health_route(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "YouTube Automation System"


def test_register_login_logout(client: TestClient):
    payload = {
        "email": "user1@example.com",
        "full_name": "User One",
        "password": "Password123",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_response.status_code == 200
    assert (
        logout_response.json()["message"]
        == "Logout successful on client by discarding JWT"
    )


def test_channel_lifecycle(client: TestClient, auth_token: str):
    response = client.post(
        "/api/v1/channels",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "Test Channel",
            "niche": "education",
            "uploads_per_day": 2,
        },
    )
    assert response.status_code == 200
    channel_id = response.json()["id"]

    list_response = client.get(
        "/api/v1/channels",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert list_response.status_code == 200
    assert any(channel["id"] == channel_id for channel in list_response.json())

    delete_response = client.delete(
        f"/api/v1/channels/{channel_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Channel deleted"


def test_generate_and_upload_video(client: TestClient, auth_token: str):
    register_payload = {
        "email": "producer@example.com",
        "full_name": "Producer",
        "password": "Password123",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )
    token = login_response.json()["access_token"]

    channel_response = client.post(
        "/api/v1/channels",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Video Channel",
            "niche": "gaming",
            "uploads_per_day": 1,
        },
    )
    channel_id = channel_response.json()["id"]

    generate_response = client.post(
        "/api/v1/videos/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel_id": channel_id, "topic": "fastapi testing"},
    )
    assert generate_response.status_code == 200
    video_id = generate_response.json()["id"]
    assert generate_response.json()["status"] == "generated"

    upload_response = client.post(
        "/api/v1/videos/upload",
        headers={"Authorization": f"Bearer {token}"},
        json={"video_id": video_id},
    )
    assert upload_response.status_code == 200
    assert upload_response.json()["message"] == "Video upload dispatched"


def test_schedule_and_queue(client: TestClient, auth_token: str):
    register_payload = {
        "email": "scheduler@example.com",
        "full_name": "Scheduler",
        "password": "Password123",
    }
    client.post("/api/v1/auth/register", json=register_payload)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )
    token = login_response.json()["access_token"]

    channel_response = client.post(
        "/api/v1/channels",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Scheduler Channel",
            "niche": "music",
            "uploads_per_day": 1,
        },
    )
    channel_id = channel_response.json()["id"]

    generate_response = client.post(
        "/api/v1/videos/generate",
        headers={"Authorization": f"Bearer {token}"},
        json={"channel_id": channel_id, "topic": "performance review"},
    )
    video_id = generate_response.json()["id"]

    schedule_response = client.post(
        "/api/v1/schedule",
        headers={"Authorization": f"Bearer {token}"},
        json={"video_id": video_id, "scheduled_at": "2099-12-31T12:00:00Z"},
    )
    assert schedule_response.status_code == 200
    assert schedule_response.json()["message"] == "Video scheduled"

    queue_response = client.get(
        "/api/v1/queue",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert queue_response.status_code == 200
    assert any(item["video_id"] == video_id for item in queue_response.json())


def test_admin_endpoints_require_admin(client: TestClient, auth_token: str):
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 403


def test_admin_stats_access(client: TestClient, admin_token: str):
    response = client.get(
        "/api/v1/admin/system-status",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["analytics"]["workers_online"] is True


def test_security_headers_are_present(client: TestClient, auth_token: str):
    response = client.get(
        "/api/v1/channels",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    assert response.headers["Strict-Transport-Security"]
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert response.headers["Permissions-Policy"] == "geolocation=(), microphone=()"
    assert response.headers["Content-Security-Policy"] == "default-src 'self'"
