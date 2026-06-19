def test_analytics_summary_uses_current_user_data(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    channel = client.post(
        "/api/v1/channels",
        json={"name": "Analytics Channel", "niche": "education"},
        headers=headers,
    ).json()
    client.post(
        "/api/v1/videos/generate",
        json={"topic": "analytics topic", "channel_id": channel["id"]},
        headers=headers,
    )

    response = client.get("/api/v1/analytics/summary", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "channels": 1,
        "videos": 1,
        "scheduled": 0,
        "views": 0,
        "likes": 0,
        "comments": 0,
    }
