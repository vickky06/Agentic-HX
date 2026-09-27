# src/domain/enums/agent_enum_builder.py
from enum import Enum
from typing import Dict, Any, Type

def build_agent_type_enum(config_data: Dict[str, Any], base: Type[Enum] = Enum) -> Type[Enum]:
    """Dynamically build an AgentType Enum from config."""
    agent_types = config_data.get("agent_types", [])
    if not agent_types:
        raise ValueError("No agent_types found in configuration.")

    enum_members = {agent["name"]: agent["name"] for agent in agent_types}
    print(f"🧱 Building AgentType Enum with members: {list(enum_members.keys())}")

    # ✅ Only add `type=base` if base is not already an Enum subclass
    if issubclass(base, Enum):
        DynamicAgentType = Enum("AgentType", enum_members)
    else:
        DynamicAgentType = Enum("AgentType", enum_members, type=base)

    return DynamicAgentType
