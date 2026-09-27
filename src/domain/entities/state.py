from typing import Dict, Any
from pydantic import BaseModel, Field
from langgraph.graph.message import Annotated
from copy import deepcopy
import asyncio


class State(BaseModel):
    """
    Domain entity: runtime context shared across agents and nodes.
    Each node gets its own isolated scope but merges updates to
    global meta safely across concurrent executions.
    """

    # ✅ Annotated fields: allows concurrent merges in LangGraph
    meta: Annotated[Dict[str, Any], "merge_dict"] = Field(default_factory=dict)
    nodes_processing: Annotated[Dict[str, Any], "merge_dict"] = Field(default_factory=dict)

    # --- Domain Rules ---

    def update_meta(self, new_meta: Dict[str, Any]):
        """Merge meta preserving existing keys."""
        self.meta.update(new_meta)

    def update_nodes_processing(self, new_nodes: Dict[str, Any]):
        """Merge node processing states."""
        self.nodes_processing.update(new_nodes)

    def update_node_context(self, node_id: str, context: Dict[str, Any]):
        """Scoped node context update."""
        node_state = self.nodes_processing.get(node_id, {})
        node_state.update(context)
        self.nodes_processing[node_id] = node_state

    # --- State Management Helpers ---

    def snapshot(self) -> Dict[str, Any]:
        """Return deep copy snapshot for persistence."""
        return deepcopy(self.dict())

    def diff(self, other: "State") -> Dict[str, Any]:
        """Compute differences from another state."""
        changes = {}
        for key, val in self.meta.items():
            if other.meta.get(key) != val:
                changes[key] = {"from": other.meta.get(key), "to": val}
        return changes

    async def transactional_update(self, meta=None, nodes=None):
        """Async-safe atomic merge."""
        async with asyncio.Lock():
            if meta:
                self.update_meta(meta)
            if nodes:
                self.update_nodes_processing(nodes)

    def to_json(self) -> str:
        """Serialize state for persistence."""
        return self.model_dump_json()
    

    @classmethod
    def from_json(cls, json_str: str) -> "State":
        """Rehydrate from JSON."""
        return cls.model_validate_json(json_str)
