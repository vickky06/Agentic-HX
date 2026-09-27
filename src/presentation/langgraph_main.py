# src/presentation/main.py
import asyncio
from typing import List
from src.application.dtos.graph_dto import EdgeDTO, GraphDTO, Node
from src.domain.entities.state import State
from src.domain.enums.agent_enum_builder import build_agent_type_enum
from src.infrastructure.configs.config_init import ConfigInit
from src.infrastructure.factory.agent_factory import AgentFactory
from src.infrastructure.orchestrator.graph_orchestrator import GraphOrchestrator

async def lang_graph_main():
    config = ConfigInit()
    AgentType = build_agent_type_enum(config.config)

    # Register all agents from YAML
    for agent in config.agent_types:
        AgentFactory.register(AgentType(agent["name"]), agent["class"])
    graph = GraphDTO(
    name="RAG Pipeline",
    nodes=[
        Node(
            node_name="evaluator",
            node_id=5,
            node_type="RETRIEVER_AGENT",
            edges=[],  # or add further edges if needed
        ),
        Node(
            node_name="retriever_1",
            node_id=1,
            node_type="RETRIEVER_AGENT",
            edges=[EdgeDTO(from_node="retriever_1", to_node="llm")],
        ),
        Node(
            node_name="retriever_2",
            node_id=2,
            node_type="RETRIEVER_AGENT",
            edges=[EdgeDTO(from_node="retriever_2", to_node="llm")],
        ),
        Node(
            node_name="llm",
            node_id=3,
            node_type="LLM_AGENT",
            edges=[
                EdgeDTO(from_node="llm", to_node="human"),
                EdgeDTO(from_node="llm", to_node="evaluator"),
            ],
        ),
        Node(
            node_name="human",
            node_id=4,
            node_type="HUMAN_AGENT",
            edges=[],
        ),
    ],
)


    # Initial state
    state = State(meta={"query": "Large Language Models"})

    # Execute
    orchestrator = GraphOrchestrator()
    final_state = await orchestrator.execute_graph(graph, state)

    # print("\n📦 Final State Snapshot:", final_state.snapshot())

