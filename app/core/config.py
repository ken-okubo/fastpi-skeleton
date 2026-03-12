import logging
import os
from functools import lru_cache

from pydantic import computed_field, model_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Database
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "myapp"
    environment: str = "dev"

    # JWT
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @computed_field
    @property
    def database_url(self) -> str:
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            if env_url.startswith("postgres://"):
                env_url = env_url.replace("postgres://", "postgresql://", 1)
            return env_url
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.environment.lower() in ("prod", "production")

    @computed_field
    @property
    def is_development(self) -> bool:
        return self.environment.lower() in ("dev", "development", "local")

    @model_validator(mode="after")
    def validate_production_settings(self):
        """Validate critical settings for production environment."""
        if self.is_production:
            if self.secret_key == "change-me-in-production":
                raise ValueError(
                    "Production environment requires a secure SECRET_KEY."
                )
        return self

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
