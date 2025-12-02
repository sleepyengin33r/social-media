from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Single class configuration following 12-factor app methodology.
    All config is injected via environment variables - ideal for cloud-native apps.

    In cloud environments (K8s, Docker, AWS, etc.), set env vars directly.
    For local development, use a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ===================
    # Application
    # ===================
    ENV: Literal["development", "staging", "production", "testing"] = "development"
    APP_NAME: str = "Social Media API"
    DEBUG: bool = False

    # ===================
    # Database
    # ===================
    DATABASE_URL: str = "sqlite:///./app.db"

    # ===================
    # Security
    # ===================
    SECRET_KEY: str = "change-me-in-production"

    # ===================
    # Computed Properties
    # ===================
    @computed_field
    @property
    def is_development(self) -> bool:
        return self.ENV == "development"

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    @computed_field
    @property
    def is_testing(self) -> bool:
        return self.ENV == "testing"


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance (singleton pattern).
    Use this function for dependency injection in FastAPI.
    """
    return Settings()


# Direct import convenience: from api.config import settings
settings = get_settings()
