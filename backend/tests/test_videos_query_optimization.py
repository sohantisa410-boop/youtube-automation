from fastapi.testclient import TestClient


def test_video_list_query_uses_channel_join(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/v1/videos", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
