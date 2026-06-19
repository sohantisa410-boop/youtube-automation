from app.core.config import settings


def get_worker_health() -> dict[str, str | bool]:
    if settings.redis_url == "memory://":
        return {"workers_online": True, "broker": "memory", "status": "ok"}

    try:
        import redis

        client = redis.Redis.from_url(
            settings.redis_url,
            socket_connect_timeout=1,
            socket_timeout=1,
        )
        client.ping()
    except Exception:
        return {"workers_online": False, "broker": "redis", "status": "unavailable"}

    return {"workers_online": True, "broker": "redis", "status": "ok"}
