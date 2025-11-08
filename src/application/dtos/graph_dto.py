# src/application/dtos/graph_dto.py
from pydantic import BaseModel, Field
from typing import List, Optional

class EdgeDTO(BaseModel):
    """Represents a directional edge in the graph."""
    from_node: str = Field(..., description="Name of the source node")
    to_node: str = Field(..., description="Name of the destination node")

class Node(BaseModel):
    """Represents an agent node in the graph."""
    node_name: str = Field(..., description="Unique name of the node (used in execution)")
    node_id: int = Field(..., description="Numeric ID of the node")
    node_type: str = Field(..., description="Type of agent (matches AgentType)")
    edges: List[EdgeDTO] = Field(default_factory=list, description="List of outgoing edges from this node")

class GraphDTO(BaseModel):
    """Graph definition containing nodes and their relationships."""
    name: str = Field(..., description="Name of the graph")
    nodes: List[Node] = Field(..., description="List of nodes participating in this graph")
