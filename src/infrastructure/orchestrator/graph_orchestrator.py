# src/infrastructure/orchestrator/graph_orchestrator.py
from langgraph.graph import StateGraph, END, START
from src.infrastructure.factory.agent_factory import AgentFactory
from src.infrastructure.orchestrator.node_runtime import NodeRuntime
from src.domain.entities.state import State
from src.application.dtos.graph_dto import GraphDTO


class GraphOrchestrator:
    def __init__(self):
        self.factory = AgentFactory()

    def _build_state_graph(self, graph_dto: GraphDTO) -> StateGraph:
        """Builds a LangGraph DAG using add_node/add_edge API."""
        g = StateGraph(State)
        
        print(f"\n🧩 Building StateGraph for: {graph_dto.name}")

        all_nodes = {node.node_name for node in graph_dto.nodes}
        all_targets = set()

        # --- Add nodes ---
        for node in graph_dto.nodes:
            agent = self.factory.create(node)
            node_name = node.node_name
            async def _agent_node(state: State, _agent=agent, _name=node_name):
                print(f"🚀 Executing agent: {_name}")
                runtime = NodeRuntime(_name, _agent)
                return await runtime.execute(state)

            g.add_node(node_name, _agent_node)
            print(f"   🔧 Added node: {node_name}")

        # --- Validate edges before adding ---
        for node in graph_dto.nodes:
            for edge in node.edges:
                if edge.to_node not in all_nodes:
                    raise ValueError(
                        f"⚠️ Invalid edge: `{edge.from_node} → {edge.to_node}` "
                        f"(Target `{edge.to_node}` does not exist in graph)"
                    )

        # --- Add edges ---
        for node in graph_dto.nodes:
            for edge in node.edges:
                if edge.from_node and edge.to_node:
                    g.add_edge(edge.from_node, edge.to_node)
                    all_targets.add(edge.to_node)
                    print(f"   🔗 Edge: {edge.from_node} → {edge.to_node}")

            if not node.edges:
                g.add_edge(node.node_name, END)
                print(f"   🏁 Terminal node: {node.node_name} → END")

        # --- Add START connections ---
        root_nodes = all_nodes - all_targets
        for root in root_nodes:
            g.add_edge(START, root)
            print(f"   🚀 Entry node: START → {root}")

        return g
    async def execute_graph(self, graph_dto: GraphDTO, state: State) -> State:
        g = self._build_state_graph(graph_dto)
        print(f"\n🏗️ Compiling graph: {graph_dto.name}")

        app = g.compile()
        
        print(f"\n🚀 Executing compiled graph: {graph_dto.name}")

        # Convert to dict before invoke, rebuild after
        result = await app.ainvoke(state.model_dump())
        state = State(**result)

        print(f"\n🏁 Graph '{graph_dto.name}' completed.")
        print("📦 Final State Snapshot:", state.model_dump())
        return state
