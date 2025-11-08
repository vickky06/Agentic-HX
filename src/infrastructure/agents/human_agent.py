# src/infrastructure/agents/human_agent.py
from src.infrastructure.agents.base_agent import BaseAgent
from src.domain.entities.state import State

class HumanAgent(BaseAgent):
    def __init__(self, name=None):
        super().__init__(name)
    async def run(self, state: State) -> State:
        summary = (
            state.nodes_processing.get("llm", {}).get("summary")
            or state.meta.get("llm_output")
            or "<no summary available>"
        )
        print(f"\n🧍 Human review needed for summary:\n{summary}\n")

        # Simulated feedback
        feedback = "Looks good! ✅"
        state.update_nodes_processing({"human": {"feedback": feedback}})

        print("🗒️ Human feedback recorded:", feedback)
        return state
