# flake8: noqa: E402
import os

import pytest
from fastapi.testclient import TestClient

os.environ["APP_ENV"] = "testing"  # noqa: E402
os.environ["TESTING"] = "true"  # noqa: E402
os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # noqa: E402
os.environ["REDIS_URL"] = "memory://"  # noqa: E402
os.environ["SECRET_KEY"] = "test-secret-key"  # noqa: E402

from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.base import Base  # noqa: E402
from app.models.user import User, UserRole


@pytest.fixture(scope="function")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides.clear()
    with TestClient(app) as client_instance:
        yield client_instance


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def auth_token(client):
    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "strongpass",
    }
    client.post("/api/v1/auth/register", json=payload)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def admin_token(client):
    db = SessionLocal()
    user = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpass"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass"},
    )
    return response.json()["access_token"]
