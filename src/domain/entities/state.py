from typing import Dict, Any
from pydantic import BaseModel, Field

class State(BaseModel):
    meta: Dict[str, Any] = Field(default_factory=dict)
    nodes_processing: Dict[str, Any] = Field(default_factory=dict)

    def update_meta(self, new_meta: Dict[str, Any]):
        """Domain rule: merge meta preserving old keys"""
        self.meta.update(new_meta)

    def update_nodes_processing(self, new_nodes: Dict[str, Any]):
        """Domain rule: merge processing nodes"""
        self.nodes_processing.update(new_nodes)