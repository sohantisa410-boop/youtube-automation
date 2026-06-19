from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "YouTube Automation System"
    app_env: str = "development"
    testing: bool = False
    api_v1_prefix: str = "/api/v1"
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/youtube_automation"
    )
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:5173"
    rate_limit_per_minute: int = 120
    storage_provider: str = "local"
    storage_bucket: str = ""
    storage_region: str = ""
    storage_base_url: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""
    log_level: str = "INFO"
    sentry_dsn: str | None = None
    security_csp: str = "default-src 'self'"
    security_frame_options: str = "DENY"
    security_content_type_options: str = "nosniff"
    security_referrer_policy: str = "strict-origin-when-cross-origin"
    security_permissions_policy: str = "geolocation=(), microphone=()"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

if settings.app_env == "production" and (
    not settings.secret_key
    or settings.secret_key == "CHANGE_ME_IN_PRODUCTION"
):
    raise RuntimeError(
        "SECRET_KEY must be configured before starting the application in production. "
        "Update backend/.env or render.yaml with a strong secret."
    )
