from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/learnapp"
    redis_url: str = "redis://localhost:6379/0"
    encryption_key: str = "change-me-32-bytes-min"
    session_secret: str = "change-me-session-secret"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
