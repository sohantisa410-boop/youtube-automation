def test_channels_crud(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # create channel
    payload = {"name": "Test Channel", "niche": "tech"}
    r = client.post("/api/v1/channels", json=payload, headers=headers)
    assert r.status_code == 200
    ch = r.json()
    assert ch["name"] == payload["name"]

    # list channels
    r2 = client.get("/api/v1/channels", headers=headers)
    assert r2.status_code == 200
    assert any(c["id"] == ch["id"] for c in r2.json())

    # delete channel
    r3 = client.delete(f"/api/v1/channels/{ch['id']}", headers=headers)
    assert r3.status_code == 200
    assert "deleted" in r3.json()["message"].lower()


def test_video_generate_and_upload(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # create channel
    payload = {"name": "Upload Channel", "niche": "music"}
    r = client.post("/api/v1/channels", json=payload, headers=headers)
    ch = r.json()

    # generate video
    gen_payload = {"topic": "test topic", "channel_id": ch["id"]}
    r2 = client.post("/api/v1/videos/generate", json=gen_payload, headers=headers)
    assert r2.status_code == 200
    video = r2.json()
    assert "title" in video and video["status"]

    # upload video
    r3 = client.post(
        "/api/v1/videos/upload",
        json={"video_id": video["id"]},
        headers=headers,
    )
    assert r3.status_code == 200
    assert "dispatched" in r3.json()["message"].lower()
