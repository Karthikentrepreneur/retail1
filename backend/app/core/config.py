from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):
    environment: str = Field(default="dev")
    api_prefix: str = Field(default="/api")
    secret_key: str = Field(default="change-me")
    session_secret: str = Field(default="change-me-too")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_minutes: int = Field(default=60 * 24 * 7)
    algorithm: str = Field(default="HS256")

    database_url: str = Field(default="postgresql+asyncpg://user:pass@localhost:5432/pos")
    sync_database_url: str = Field(default="postgresql+psycopg://user:pass@localhost:5432/pos")
    redis_url: str = Field(default="redis://localhost:6379/0")

    cors_origins: List[AnyHttpUrl] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:5173"])

    otp_provider_url: str | None = None
    payment_gateway_api_key: str | None = None
    payment_gateway_secret: str | None = None
    gsp_api_key: str | None = None
    gsp_api_secret: str | None = None

    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_prefix = "POS_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
