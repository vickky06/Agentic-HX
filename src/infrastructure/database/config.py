"""Database configuration."""

from pydantic import Field
from src.infrastructure.configs.config_init import ConfigInit


class DatabaseConfig(ConfigInit):
    model_config = ConfigInit.model_config
    
    host: str = Field(default="localhost", validation_alias="DB_HOST")
    port: int = Field(default=5432, validation_alias="DB_PORT")
    name: str = Field(default="hexagonal_db", validation_alias="DB_NAME")
    user: str = Field(default="user", validation_alias="DB_USER")
    password: str = Field(default="password", validation_alias="DB_PASSWORD")
    echo: bool = Field(default=False, validation_alias="DB_ECHO")

    @property
    def url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"