# from src.infrastructure.agents.llm_agent import LlmAgent
# from src.infrastructure.agents.human_agent import HumanAgent
# from src.infrastructure.agents.retriever_agent import RetrieverAgent
import importlib
from src.application.dtos.graph_dto import Node
from src.domain.enums import AgentType


# class AgentFactory:
#     _registry = {
#         "retriever": RetrieverAgent,
#         "llm": LlmAgent,
#         "human": HumanAgent,
#     }

#     @classmethod
#     def create(cls, agent_name: str):
#         if agent_name not in cls._registry:
#             raise ValueError(f"Agent '{agent_name}' not registered.")
#         return cls._registry[agent_name]()

# src/infrastructure/factory/agent_factory.py

# src/infrastructure/factory/agent_factory.py
# src/infrastructure/factory/agent_factory.py
import importlib
from typing import Type, Any, Union
from src.domain.enums import AgentType        # ← ensure this imports your dynamically generated Enum
from src.infrastructure.agents.base_agent import BaseAgent  # ← all agents inherit this

class AgentFactory:
    # ✅ Correct typing — store only subclasses of BaseAgent
    _registry: dict[str, Type[BaseAgent]] = {}

    @classmethod
    def register(cls, agent_type: AgentType, class_path: str): # type: ignore
        """Register an agent class path under a given agent type."""
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        agent_cls = getattr(module, class_name)

        # ✅ Validation — only allow classes inheriting BaseAgent
        if not issubclass(agent_cls, BaseAgent):
            raise TypeError(f"❌ {class_path} must inherit from BaseAgent")

        cls._registry[agent_type.value] = agent_cls
        print(f"✅ Registered {agent_type.value} -> {class_path}")

    @classmethod
    def create(cls, agent:Node , *args, **kwargs) -> BaseAgent: 
        """Create an instance of a registered agent by type or enum."""
        agent_type = agent.node_type
        if agent_type not in cls._registry:
            raise ValueError(f"❌ Agent type '{agent_type}' not registered.")
        agent_cls = cls._registry[agent_type]
        return agent_cls(*args, **kwargs)
