from src.infrastructure.agents.base_agent import BaseAgent
from src.domain.entities.state import State

class RetrieverAgent(BaseAgent):
    def __init__(self, name=None):
        super().__init__(name)
    async def run(self, state: State) -> State:
        query = state.meta.get("query")
        docs = [f"Doc about {query} 1", f"Doc about {query} 2"]
        state.update_nodes_processing({"retriever": {"docs": docs}})
        print("🔍 RetrieverAgent retrieved docs:", docs)
        return state
