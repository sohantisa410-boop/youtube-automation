from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

engine_kwargs: dict[str, Any] = {
    "pool_pre_ping": True,
}
connect_args: dict[str, Any] = {}

if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False
    if settings.database_url == "sqlite:///:memory:":
        engine_kwargs["poolclass"] = StaticPool  # type: ignore[assignment]

engine = create_engine(
    settings.database_url, connect_args=connect_args, **engine_kwargs
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
