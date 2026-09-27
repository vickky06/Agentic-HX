from abc import ABC, abstractmethod
from domain.entities.state import State

class StateRepository(ABC):
    @abstractmethod
    async def load_state(self, run_id: str) -> State | None:
        """Load the state for a given run_id."""
        pass

    @abstractmethod
    async def save_state(self, run_id: str, state: State) -> None:
        """Persist the state snapshot for a run_id."""
        pass
