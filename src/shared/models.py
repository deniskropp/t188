from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

# Base Graph Elements
# Base Graph Elements

class KeyValue(BaseModel):
    key: str
    value: str

class GraphNode(BaseModel):
    id: str
    type: str
    properties: List[KeyValue] = Field(default_factory=list)

    @field_validator('properties', mode='before')
    @classmethod
    def validate_properties(cls, v: Any) -> Any:
        if isinstance(v, dict):
            return [KeyValue(key=k, value=str(val)) for k, val in v.items()]
        return v

class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    properties: List[KeyValue] = Field(default_factory=list)

    @field_validator('properties', mode='before')
    @classmethod
    def validate_properties(cls, v: Any) -> Any:
        if isinstance(v, dict):
            return [KeyValue(key=k, value=str(val)) for k, val in v.items()]
        return v

# KickLang Command Payloads

class StoryRequest(BaseModel):
    """Payload for <<story_request>>"""
    user_input: str

class WorldState(BaseModel):
    """Payload for <<world_state>>"""
    locations: List[str] = Field(default_factory=list, description="Names of locations discovered")
    concepts: List[str] = Field(default_factory=list, description="Abstract concepts or lore elements")
    items: List[str] = Field(default_factory=list, description="Physical objects or items of interest")
    
    nodes: List[GraphNode] = Field(default_factory=list, description="Full node details for locations, concepts, items")
    edges: List[GraphEdge] = Field(default_factory=list, description="Relationships like 'located_in' or 'possesses'")

class CharacterUpdate(BaseModel):
    """Payload for <<character_update>>"""
    characters: List[str] = Field(default_factory=list, description="Names of characters involved")
    
    nodes: List[GraphNode] = Field(default_factory=list, description="Full node details for characters")
    edges: List[GraphEdge] = Field(default_factory=list, description="Relationships like 'has_trait', 'interacts_with', 'possesses'")

class PlotPoint(BaseModel):
    """Payload for <<plot_point>>"""
    events: List[str] = Field(default_factory=list, description="Short descriptions of events")
    
    nodes: List[GraphNode] = Field(default_factory=list, description="Full node details for events")
    edges: List[GraphEdge] = Field(default_factory=list, description="Relationships like 'precedes'")

class SynthesisOutput(BaseModel):
    """Payload for <<synthesis_output>>"""
    narrative_segment: str

class Feedback(BaseModel):
    """Payload for Critic's evaluation"""
    score: float # 0.0 to 1.0
    critique: str
    suggestion: str
    approved: bool

class SuggestionList(BaseModel):
    """Payload for dynamic story suggestions"""
    suggestions: List[str] = Field(..., description="A list of creative story starting prompts")
