import pytest
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.skipif(
    settings.redis_url.startswith("memory://"),
    reason="Memory redis backend does not support actual connection test",
)
def test_redis_connection():
    import redis

    client = redis.from_url(settings.redis_url)
    assert client.ping() is True
