"""Database configuration."""


from pydantic import Field
from src.infrastructure.configs.config_init import ConfigInit


class DatabaseConfig(ConfigInit):

    host: str = Field(default="localhost", alias="DB_HOST")
    port: int = Field(default=5432, alias="DB_PORT")
    name: str = Field(default="hexagonal_db", alias="DB_NAME")
    user: str = Field(default="user", alias="DB_USER")
    password: str = Field(default="password", alias="DB_PASSWORD")
    echo: bool = Field(default=False, alias="DB_ECHO")

    
    @property
    def url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"