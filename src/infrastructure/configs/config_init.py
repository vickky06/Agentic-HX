from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
class ConfigInit(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,  # Add this
    )

    app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")
    app_log_level: str = Field(default="info", validation_alias="APP_LOG_LEVEL")
    app_reload: bool = Field(default=True, validation_alias="APP_RELOAD")

    @property
    def uvicorn_config(self) -> dict:
        return {
            "host": self.app_host,
            "port": self.app_port,
            "log_level": self.app_log_level,
            "reload": self.app_reload,      
        }