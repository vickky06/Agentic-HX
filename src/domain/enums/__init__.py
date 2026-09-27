# src/domain/enums/__init__.py
from enum import Enum
from src.infrastructure.configs.config_init import ConfigInit
from src.domain.enums.agent_enum_builder import build_agent_type_enum

class AgentTypeBase(str, Enum):
    """Base class for all AgentType enums."""
    pass

config = ConfigInit()
AgentType = build_agent_type_enum(config.config, base=AgentTypeBase)
