from abc import ABC, abstractmethod
from src.domain.entities.state import State
from src.application.dtos.graph_dto import GraphDTO

class OrchestratorPort(ABC):
    @abstractmethod
    async def execute_graph(self, graph: GraphDTO, state: State) -> State:
        pass
