from datetime import datetime, timedelta, timezone


def test_schedule_and_queue(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # create channel and video
    payload = {"name": "Sched Channel", "niche": "gaming"}
    ch = client.post("/api/v1/channels", json=payload, headers=headers).json()

    gen_payload = {"topic": "schedule topic", "channel_id": ch["id"]}
    video = client.post(
        "/api/v1/videos/generate", json=gen_payload, headers=headers
    ).json()

    scheduled_at = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    r = client.post(
        "/api/v1/schedule",
        json={"video_id": video["id"], "scheduled_at": scheduled_at},
        headers=headers,
    )
    assert r.status_code == 200

    # list queue
    r2 = client.get("/api/v1/queue", headers=headers)
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)


def test_duplicate_schedule_is_rejected(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    channel = client.post(
        "/api/v1/channels",
        json={"name": "Duplicate Schedule", "niche": "tech"},
        headers=headers,
    ).json()
    video = client.post(
        "/api/v1/videos/generate",
        json={"topic": "duplicate topic", "channel_id": channel["id"]},
        headers=headers,
    ).json()
    payload = {
        "video_id": video["id"],
        "scheduled_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }

    first = client.post("/api/v1/schedule", json=payload, headers=headers)
    assert first.status_code == 200

    second = client.post("/api/v1/schedule", json=payload, headers=headers)
    assert second.status_code == 400
    assert second.json()["detail"] == "Video is already scheduled"


def test_only_generated_videos_can_be_scheduled(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    channel = client.post(
        "/api/v1/channels",
        json={"name": "Upload Before Schedule", "niche": "music"},
        headers=headers,
    ).json()
    video = client.post(
        "/api/v1/videos/generate",
        json={"topic": "uploaded topic", "channel_id": channel["id"]},
        headers=headers,
    ).json()
    upload_response = client.post(
        "/api/v1/videos/upload",
        json={"video_id": video["id"]},
        headers=headers,
    )
    assert upload_response.status_code == 200

    schedule_response = client.post(
        "/api/v1/schedule",
        json={
            "video_id": video["id"],
            "scheduled_at": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat(),
        },
        headers=headers,
    )
    assert schedule_response.status_code == 400
    assert (
        schedule_response.json()["detail"]
        == "Only generated videos can be scheduled"
    )
