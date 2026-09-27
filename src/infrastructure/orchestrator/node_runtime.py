# src/infrastructure/orchestrator/node_runtime.py
from src.domain.entities.state import State

class NodeRuntime:
    def __init__(self, agent_name, agent):
        self.agent_name = agent_name
        self.agent = agent

    async def execute(self, state: State) -> State:
        print(f"\n🚀 Executing node: {self.agent_name}")
        try:
            new_state = await self.agent.run(state)
            print(f"✅ Node {self.agent_name} completed.")
            return new_state
        except Exception as e:
            print(f"❌ Node {self.agent_name} failed: {e}")
            raise
