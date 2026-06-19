import logging

import pytest
from fastapi.testclient import TestClient


def test_admin_users_and_stats(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}

    users_response = client.get("/api/v1/admin/users", headers=headers)
    assert users_response.status_code == 200
    users = users_response.json()
    assert isinstance(users, list)
    assert any(user["email"] == "admin@example.com" for user in users)

    status_response = client.get("/api/v1/admin/system-status", headers=headers)
    assert status_response.status_code == 200
    status = status_response.json()
    assert status["status"] == "ok"
    assert status["analytics"]["workers_online"] is True
    assert status["analytics"]["status"] == "ok"


def test_admin_counts_and_user_updates(client: TestClient, admin_token: str):
    headers = {"Authorization": f"Bearer {admin_token}"}

    videos_response = client.get("/api/v1/admin/videos", headers=headers)
    assert videos_response.status_code == 200
    assert "total_videos" in videos_response.json()

    channels_response = client.get("/api/v1/admin/channels", headers=headers)
    assert channels_response.status_code == 200
    assert "total_channels" in channels_response.json()

    register_payload = {
        "email": "stable_user@example.com",
        "full_name": "Stable User",
        "password": "Password123",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 200
    new_user_id = register_response.json()["id"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )
    assert login_response.status_code == 200

    user_id = new_user_id

    status_response = client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=headers,
        json={"is_active": False},
    )
    assert status_response.status_code == 200
    assert status_response.json()["is_active"] is False

    inactive_login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": register_payload["email"],
            "password": register_payload["password"],
        },
    )
    assert inactive_login_response.status_code == 401
    assert inactive_login_response.json()["detail"] == "User not found or inactive"

    plan_response = client.patch(
        f"/api/v1/admin/users/{user_id}/plan",
        headers=headers,
        json={"plan": "pro"},
    )
    assert plan_response.status_code == 200
    assert plan_response.json()["plan"] == "pro"


def test_admin_non_admin_forbidden(
    client: TestClient, auth_token: str, caplog: pytest.LogCaptureFixture
):
    caplog.set_level(logging.INFO, logger="app.core.exceptions")

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/v1/admin/users", headers=headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "Admin access required"}
    assert "HTTP error for /api/v1/admin/users: Admin access required" in caplog.text
    assert not any(
        record.levelno >= logging.WARNING
        and record.name == "app.core.exceptions"
        and "Admin access required" in record.getMessage()
        for record in caplog.records
    )
