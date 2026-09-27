class OrchestratorService:
    def __init__(self, orchestrator_port):
        self.orchestrator = orchestrator_port

    async def run_graph(self, graph_dto, state):
        final_state = await self.orchestrator.execute_graph(graph_dto, state)
        return final_state
