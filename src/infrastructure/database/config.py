"""Database configuration."""

import os
from pydantic import Field
from src.infrastructure.configs.config_init import ConfigInit


class DatabaseConfig(ConfigInit):
    model_config = ConfigInit.model_config

    db_type: str = Field(default="postgresql", validation_alias="DEFAULT_DB_TYPE")
    host: str = Field(default="localhost", validation_alias="DB_HOST")
    port: int = Field(default=5432, validation_alias="DB_PORT")
    db_name: str = Field(default="agentic_db", validation_alias="DB_NAME")
    user: str = Field(default="viveksingh", validation_alias="DB_USER")
    password: str = Field(default="password", validation_alias="DB_PASSWORD")
    echo: bool = Field(default=False, validation_alias="DB_ECHO")
    min_size: int = Field(default=1, validation_alias="DB_MIN_SIZE")
    max_size: int = Field(default=5, validation_alias="DB_MAX_SIZE")

    @property
    def url(self) -> str:
        """Get the async database connection URL."""
        # Allow DATABASE_URL override (e.g. from Alembic or environment)
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url 
        

        # If running inside Docker, host should be 'db'
        dockerized_host = "db" if os.getenv("DOCKER_ENV", "false").lower() == "true" else self.host

        # Use asyncpg driver for async SQLAlchemy
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{dockerized_host}:{self.port}/{self.db_name}"
        )