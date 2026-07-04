"""Environment-backed application settings."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import API_VERSION, SERVICE_NAME


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local .env file."""

    APP_NAME: str = SERVICE_NAME
    APP_VERSION: str = API_VERSION
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    DATABASE_URL: str | None = None
    REDIS_URL: str | None = None
    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("DATABASE_URL", "REDIS_URL", "JWT_SECRET_KEY", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        """Treat blank optional environment variables as unconfigured."""

        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def cors_origins(self) -> list[str]:
        """Return the comma-separated CORS setting as a clean list."""

        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def database_configured(self) -> bool:
        """Return True only when a non-empty database URL is configured."""

        return bool(self.DATABASE_URL and self.DATABASE_URL.strip())


@lru_cache
def get_settings() -> Settings:
    """Create settings once per process."""

    return Settings()
