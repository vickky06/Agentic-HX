# src/config/config_init.py
import os, yaml
from pathlib import Path
from typing import Any, Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigInit(BaseSettings):
    """Unified configuration that merges .env + YAML + defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True,
    )

    # === Base system ===
    app_name: str = Field(default="Agentic-HX", validation_alias="APP_NAME")
    app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")
    app_log_level: str = Field(default="info", validation_alias="APP_LOG_LEVEL")
    app_reload: bool = Field(default=True, validation_alias="APP_RELOAD")
    yaml_config_path: str = Field(default="./config.yaml", validation_alias="APP_CONFIG_FILE")

    # === Framework / Agents ===
    agent_types: list[dict[str, Any]] = Field(default_factory=list)
    orchestrator: Dict[str, Any] = Field(default_factory=dict)
    db_config: Dict[str, Any] = Field(default_factory=dict)

    # === Common property ===
    _merged_data: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_and_merge_sources()

    def _load_and_merge_sources(self):
        """Merge defaults, YAML, and .env into one unified dict."""
        base_data = self.model_dump()
        yaml_data = self._load_yaml()
        env_data = self._load_env_overrides()

        merged = {**base_data, **yaml_data, **env_data}
        self._merged_data = merged

        # also sync object attributes so config.<key> works seamlessly
        for k, v in merged.items():
            setattr(self, k, v)

    def _load_yaml(self) -> Dict[str, Any]:
        path = Path(self.yaml_config_path)
        if path.exists():
            with open(path, "r") as f:
                data = yaml.safe_load(f) or {}
            print(f"📘 Loaded YAML config from {path}")
            return data
        print(f"⚠️ No YAML config found at {path}, skipping.")
        return {}

    def _load_env_overrides(self) -> Dict[str, Any]:
        """Optionally collect extra envs beyond BaseSettings parsing."""
        env_data = {}
        for key, value in os.environ.items():
            if key.startswith("APP_") or key.startswith("DB_"):
                env_data[key.lower().replace("app_", "").replace("db_", "db_")] = value
        return env_data

    @property
    def config(self) -> Dict[str, Any]:
        print("all config")
        """Expose final merged config."""
        return self._merged_data

    @property
    def uvicorn_config(self) -> dict:
        return {
            "host": self.app_host,
            "port": self.app_port,
            "log_level": self.app_log_level,
            "reload": self.app_reload,
        }
