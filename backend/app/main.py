import importlib
from contextlib import asynccontextmanager
from typing import Any, cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.logging_config import setup_logging
from app.core.middleware import (
    BasicRateLimitMiddleware,
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
)
from app.db.session import engine
from app.models import *  # noqa: F401,F403
from app.models.base import Base

sentry_sdk: Any | None = None
SentryAsgiMiddleware: Any | None = None

try:
    sentry_sdk = importlib.import_module("sentry_sdk")  # type: ignore
    _sentry_asgi = importlib.import_module(
        "sentry_sdk.integrations.asgi"
    )  # type: ignore
    SentryAsgiMiddleware = _sentry_asgi.SentryAsgiMiddleware
except ImportError:  # pragma: no cover - optional dependency
    sentry_sdk = None
    SentryAsgiMiddleware = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.app_env in {"development", "testing"} or settings.testing:
        Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    setup_logging()

    if settings.sentry_dsn and sentry_sdk is not None:
        sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)

    app: FastAPI = FastAPI(title=settings.app_name, lifespan=lifespan)
    add_exception_handlers(app)

    origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
    allow_all_origins = origins == ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if allow_all_origins else origins,
        allow_credentials=False if allow_all_origins else True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(BasicRateLimitMiddleware)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    if settings.sentry_dsn and SentryAsgiMiddleware is not None:
        app = cast(FastAPI, SentryAsgiMiddleware(app))

    @app.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "healthy",
            "service": settings.app_name,
            "environment": settings.app_env,
        }

    return app


app = create_app()
