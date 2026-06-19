def test_register_and_login(client):
    payload = {
        "email": "user@example.com",
        "full_name": "User Test",
        "password": "password123",
    }
    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == payload["email"]

    r2 = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert r2.status_code == 200
    token = r2.json().get("access_token")
    assert token


def test_logout_requires_auth(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.post("/api/v1/auth/logout", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"].lower().startswith("logout")


def test_authenticated_profile(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    r = client.get("/api/v1/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"


def test_inactive_token_holder_receives_401(client, auth_token, admin_token):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    user_headers = {"Authorization": f"Bearer {auth_token}"}

    users_response = client.get("/api/v1/admin/users", headers=admin_headers)
    assert users_response.status_code == 200
    user_id = next(
        user["id"]
        for user in users_response.json()
        if user["email"] == "test@example.com"
    )

    disable_response = client.patch(
        f"/api/v1/admin/users/{user_id}/status",
        headers=admin_headers,
        json={"is_active": False},
    )
    assert disable_response.status_code == 200

    profile_response = client.get("/api/v1/auth/me", headers=user_headers)
    assert profile_response.status_code == 401
    assert profile_response.json()["detail"] == "User not found or inactive"


def test_api_key_crud(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    create = client.post(
        "/api/v1/auth/api-keys",
        json={"provider": "internal"},
        headers=headers,
    )
    assert create.status_code == 200
    api_key = create.json()
    assert api_key["provider"] == "internal"
    assert "key_value" in api_key
    assert api_key["key_masked"].startswith(api_key["key_value"][0:4])

    list_response = client.get("/api/v1/auth/api-keys", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete = client.delete(f"/api/v1/auth/api-keys/{api_key['id']}", headers=headers)
    assert delete.status_code == 200
    assert delete.json()["message"] == "API key deleted"
