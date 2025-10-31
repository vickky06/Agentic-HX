from abc import ABC, abstractmethod
from domain.entities.state import State
class StateRepository(ABC):
    @abstractmethod
    async def fetch_state(self) -> State:
        """Fetch the current state from the data source."""
        pass

    @abstractmethod
    async def save_state(self, state_data: dict) -> None:
        """Save the updated state to the data source."""
        pass
