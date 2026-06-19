# flake8: noqa: E402
import os

from fastapi.testclient import TestClient

os.environ["APP_ENV"] = "testing"  # noqa: E402
os.environ["TESTING"] = "true"  # noqa: E402
os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # noqa: E402
os.environ["REDIS_URL"] = "memory://"  # noqa: E402

from app.db.session import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.base import Base  # noqa: E402

Base.metadata.create_all(bind=engine)

with TestClient(app) as client:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "strongpass",
        },
    )
    print("status", response.status_code)
    print("body", response.text)
    print("headers", response.headers)
