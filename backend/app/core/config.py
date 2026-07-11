"""Environment-backed application settings."""

from functools import lru_cache

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import API_VERSION, SERVICE_NAME


LOCAL_DEVELOPMENT_CORS_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables or a local .env file."""

    APP_NAME: str = SERVICE_NAME
    APP_VERSION: str = API_VERSION
    ENVIRONMENT: str = "development"
    APP_ENV: str | None = None
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = ",".join(LOCAL_DEVELOPMENT_CORS_ORIGINS)
    DATABASE_URL: str | None = None
    REDIS_URL: str | None = None
    JWT_SECRET_KEY: str | None = None
    SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOG_LEVEL: str = "INFO"
    BILLING_PROVIDER_MODE: str = "test"
    RAZORPAY_MODE: str = "test"
    RAZORPAY_KEY_ID: str | None = None
    RAZORPAY_KEY_SECRET: str | None = None
    RAZORPAY_WEBHOOK_SECRET: str | None = None
    RAZORPAY_STARTER_PLAN_ID: str | None = None
    RAZORPAY_PRO_PLAN_ID: str | None = None
    RAZORPAY_CHECKOUT_ENABLED: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator(
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET_KEY",
        "SECRET_KEY",
        "APP_ENV",
        "RAZORPAY_KEY_ID",
        "RAZORPAY_KEY_SECRET",
        "RAZORPAY_WEBHOOK_SECRET",
        "RAZORPAY_STARTER_PLAN_ID",
        "RAZORPAY_PRO_PLAN_ID",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        """Treat blank optional environment variables as unconfigured."""

        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def apply_docker_compatibility_aliases(self) -> "Settings":
        """Map Compose-friendly aliases onto established application settings."""

        if self.APP_ENV:
            self.ENVIRONMENT = self.APP_ENV
        if not self.JWT_SECRET_KEY and self.SECRET_KEY:
            self.JWT_SECRET_KEY = self.SECRET_KEY
        if self.ENVIRONMENT.strip().lower() == "production":
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL is required in production.")
            if not self.JWT_SECRET_KEY:
                raise ValueError("SECRET_KEY or JWT_SECRET_KEY is required in production.")
        return self

    @property
    def cors_origins(self) -> list[str]:
        """Return explicit production origins or local-safe development origins."""

        configured_origins = [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]
        if self.ENVIRONMENT.strip().lower() == "production":
            return list(dict.fromkeys(configured_origins))
        return list(
            dict.fromkeys(
                [*configured_origins, *LOCAL_DEVELOPMENT_CORS_ORIGINS]
            )
        )

    @property
    def database_configured(self) -> bool:
        """Return True only when a non-empty database URL is configured."""

        return bool(self.DATABASE_URL and self.DATABASE_URL.strip())


@lru_cache
def get_settings() -> Settings:
    """Create settings once per process."""

    return Settings()
