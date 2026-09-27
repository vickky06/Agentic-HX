# src/infrastructure/agents/llm_agent.py
from src.infrastructure.agents.base_agent import BaseAgent
from src.domain.entities.state import State

class LlmAgent(BaseAgent):
    def __init__(self, name=None):
        super().__init__(name)
    async def run(self, state: State) -> State:
        query = state.meta.get("query")
        docs = state.nodes_processing.get("retriever", {}).get("docs", [])

        # Simulated LLM reasoning
        answer = f"LLM summary for '{query}' based on {len(docs)} docs."

        # ✅ Update both meta and nodes_processing for downstream agents
        state.update_meta({"llm_output": answer})
        state.update_nodes_processing({"llm": {"summary": answer}})

        print("🧠 LlmAgent generated summary:", answer)
        return state
