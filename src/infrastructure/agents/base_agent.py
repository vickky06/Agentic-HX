from abc import ABC, abstractmethod
from src.domain.entities.state import State

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    def __init__(self, name: str | None = None):
        self.name = name or self.__class__.__name__

    @abstractmethod
    async def run(self, state: State) -> State:
        ...
