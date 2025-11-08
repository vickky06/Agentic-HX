Factory Patter for DB

src/

 ├── domain/

 │    ├── models/

 │    │    └── user.py

 │    └── services/

 │         └── user_service.py

 │

 ├── application/

 │    ├── ports/

 │    │    └── db_port.py          # <-- Interface for DB operations <fetch,create,update,delete operation interface>

 │    └── use_cases/

 │         └── create_user_usecase.py

 │
 
 ├── infrastructure/

 │    ├── db/

 │    │    ├── factory/

 │    │    │    └── db_factory.py  # <-- Factory to get the right DB implementation <create and share correct DB instance. switch conditions>

 │    │    ├── base/

 │    │    │    └── db_instance.py # <-- Interface for DB config / base class <connect, get_session inteface>

 │    │    ├── implementations/

 │    │    │    └── pgsql.py       # <-- Concrete Postgres implementation <singelton instance for DB creation>

 │    │    └── config.py           # <-- Optional DB config loader

 │    └── logger/


 │         └── logger_adapter.py

 │
 └── presentation/

      └── api/

           └── routes/
           
                └── user_routes.py


[X]: DB Models Entities

[X] : DB_PORTS

[X]: DB_Factory

[X]: DB_Instance

[X]: implementation

    [X]: pgsql
    [X]: inMem


+-------------------------------------------+
|           Agent Orchestration Layer       |
|-------------------------------------------|
|  GraphOrchestrator   |  EventBus          |
|  StateManager        |  Middleware Engine |
+-------------------------------------------+
          | uses
          v
+-------------------------------------------+
|           Agent Runtime Layer             |
|-------------------------------------------|
|  AgentFactory  |  AgentRegistry | Plugins |
|  AgentRuntime  |  ConfigLoader  | Tracing |
+-------------------------------------------+
          | instantiates
          v
+-------------------------------------------+
|         Concrete Agent Layer              |
|-------------------------------------------|
|  LLM Agents | Tool Agents | Human Agents  |
|  Super Agents (Subgraphs)                 |
+-------------------------------------------+



src/
├── domain/
│   ├── entities/
│   │   └── state.py
│   ├── services/
│   │   └── agent_policy_service.py
│   ├── value_objects/
│   │   └── __init__.py
│   └── __init__.py
│
├── application/
│   ├── dtos/
│   │   ├── agent_dto.py
│   │   ├── graph_dto.py
│   │   └── run_dto.py
│   ├── repositories/
│   │   ├── agent_repository.py
│   │   └── state_repository.py
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── graph_service.py
│   │   └── orchestrator_service.py
│   ├── ports/
│   │   ├── agent_interface.py
│   │   ├── factory_port.py
│   │   └── orchestrator_port.py
│   └── use_cases/
│       └── run_simple_graph.py
│
├── infrastructure/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── llm_agent.py
│   │   └── human_agent.py
│   ├── factory/
│   │   └── agent_factory.py
│   ├── orchestrator/
│   │   ├── node_runtime.py
│   │   └── simple_graph_orchestrator.py
│   ├── persistence/
│   │   └── memory_state_repository.py
│   └── __init__.py
│
├── presentation/
│   ├── rest/
│   │   └── routes.py
│   ├── websockets/
│   │   └── __init__.py
│   └── main.py
│
└── __init__.py



🧩 Architectural Role Summary

Here’s the complete explanation — file by file — in tabular format 🧠👇

Layer	File	Role / Responsibility	Depends On	Implements / Used By
🟩 Application → DTOs	graph_dto.py	Defines the structure of a graph definition (nodes, edges, name). Used to pass configuration from API/UI to orchestrator.	—	Used by GraphOrchestrator, OrchestratorService
🟩 Application → Ports	orchestrator_port.py	Interface (port) that defines the contract for how an orchestrator should behave — e.g., execute a graph and return final State.	Domain State	Implemented by GraphOrchestrator
🟩 Application → Repositories	state_repository.py	Abstract base class (interface) defining persistence contract for saving/loading runtime State.	Domain State	Implemented by CheckpointRepository
🟩 Application → Services	orchestrator_service.py	Application-level coordinator. Uses the orchestrator port to execute a workflow (graph). May add policies, metrics, or checkpointing.	GraphOrchestrator (via port), StateRepository	Called by presentation layer (main.py, API)
🟩 Domain → Entities	state.py	The core runtime state model shared across all nodes and agents. Maintains metadata (meta) and node-specific data (nodes_processing).	—	Used throughout orchestrator and agents
🟩 Domain → Services	agent_policy_service.py	Domain-level rules for agent execution — e.g., validation, role-based access, or sequencing. No infra dependencies.	—	Used by GraphOrchestrator or orchestrator service (optional)
🟨 Infrastructure → Agents	base_agent.py	Abstract base for all agents. Defines interface run(state) to ensure consistent execution signature.	Domain State	Extended by all concrete agents
🟨 Infrastructure → Agents	human_agent.py	Concrete agent representing a human-in-the-loop interaction (simulated for now). Updates state with feedback.	BaseAgent	Created by AgentFactory and executed by GraphOrchestrator
🟨 Infrastructure → Agents	llm_agent.py	Concrete LLM-based agent. Simulates or wraps LLM calls. Updates state.meta with model output.	BaseAgent	Created by AgentFactory and executed by orchestrator
🟨 Infrastructure → Factory	agent_factory.py	Implements factory pattern. Registers and instantiates agents dynamically based on name (e.g., "llm", "human"). Enables plug-and-play extensibility.	BaseAgent classes	Used by GraphOrchestrator
🟨 Infrastructure → Orchestrator	checkpoint_repository.py	Concrete implementation of StateRepository. Stores State snapshots keyed by run_id. In-memory for now (can be extended to Redis/DB).	StateRepository	Used by OrchestratorService
🟨 Infrastructure → Orchestrator	graph_orchestrator.py	Implements OrchestratorPort. Builds and executes a graph of agents in sequence or parallel, maintaining state transitions. Core execution engine.	AgentFactory, NodeRuntime, State	Used by OrchestratorService
🟨 Infrastructure → Orchestrator	node_runtime.py	Thin runtime wrapper for a single agent’s execution. Responsible for calling agent.run(state) and returning the updated state.	BaseAgent	Used inside GraphOrchestrator




| **Layer**                       | **Primary Responsibility**                                                                  | **Examples in Your Code**                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Domain Layer**                | Defines core business entities and rules; no external dependencies.                         | `State`, `AgentPolicyService`                                         |
| **Application Layer**           | Coordinates use cases, defines ports (contracts), DTOs, and service orchestrations.         | `GraphDTO`, `OrchestratorService`, `StateRepository`                  |
| **Infrastructure Layer**        | Implements the technical details: agents, factories, orchestrator engine, persistence, etc. | `LlmAgent`, `HumanAgent`, `GraphOrchestrator`, `CheckpointRepository` |
| **(Future) Presentation Layer** | Exposes APIs, CLIs, or UI endpoints.                                                        | e.g., `main.py`, FastAPI route, WebSocket handler                     |


+--------------------+
|  presentation/main |
|--------------------|
|  → creates GraphDTO, State  |
|  → calls OrchestratorService.run_graph() |
+-----------+------------+
            |
            v
+-------------------------+
|  application layer      |
|-------------------------|
| OrchestratorService uses |
| GraphOrchestrator (port) |
+-----------+-------------+
            |
            v
+----------------------------+
| infrastructure/orchestrator|
|----------------------------|
| GraphOrchestrator          |
|  → uses AgentFactory        |
|  → instantiates agents      |
|  → executes NodeRuntime     |
|  → updates State            |
|  → persists checkpoints     |
+----------------------------+
            |
            v
+----------------------+
| domain/entities/state|
|----------------------|
|  State manages meta  |
|  and node-processing  |
+----------------------+

🧠 Quick Example of Responsibilities per Class
| **Class / File**       | **Acts As**            | **Key Concern**                               |
| ---------------------- | ---------------------- | --------------------------------------------- |
| `State`                | Domain Entity          | Holds and mutates orchestration context       |
| `StateRepository`      | Outbound Port          | Persistence contract for saving/loading state |
| `CheckpointRepository` | Infrastructure Adapter | Concrete persistence (in-memory checkpoints)  |
| `GraphOrchestrator`    | Core Engine            | Executes agent nodes as per `GraphDTO`        |
| `NodeRuntime`          | Runtime Adapter        | Isolated agent executor                       |
| `AgentFactory`         | Factory                | Creates agent instances dynamically           |
| `LlmAgent`             | Concrete Agent         | Example LLM behavior node                     |
| `HumanAgent`           | Concrete Agent         | Example human-in-the-loop node                |
| `OrchestratorService`  | Application Service    | Coordinates a graph execution workflow        |
| `GraphDTO`             | Data Contract          | Passes graph structure to orchestrator        |
| `AgentPolicyService`   | Domain Policy          | Defines constraints and validation            |
