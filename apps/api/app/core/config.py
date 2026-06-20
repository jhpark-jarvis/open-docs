from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "OpenDocs"
    app_name: str = "OpenDocs API"
    environment: str = "development"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg://opendocs:opendocs@db:5432/opendocs"
    nexon_open_api_key: str = ""
    nexon_open_api_base_url: str = "https://open.api.nexon.com"
    cors_origins: str = "http://localhost:3000"
    redis_url: str = "redis://redis:6379/0"
    yjs_ws_url: str = "ws://localhost:1234"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
