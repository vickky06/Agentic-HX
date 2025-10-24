from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field
class ConfigInit(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    app_log_level: str = Field(default="info", alias="APP_LOG_LEVEL")
    app_reload: bool = Field(default=True, alias="APP_RELOAD")

    @property
    def uvicorn_config(self) -> dict:
        return {
            "host": self.app_host,
            "port": self.app_port,
            "log_level": self.app_log_level,
            "reload": self.app_reload,
            
        }