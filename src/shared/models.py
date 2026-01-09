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
    locations: List[str]
    concepts: List[str]
    # Optionally include full node details if needed
    location_details: List[GraphNode] = Field(default_factory=list)
    concept_details: List[GraphNode] = Field(default_factory=list)

class CharacterUpdate(BaseModel):
    """Payload for <<character_update>>"""
    characters: List[str]
    traits: List[str]
    interactions: List[str] # Format: "CharA interacts_with CharB"
    
    character_details: List[GraphNode] = Field(default_factory=list)

class PlotPoint(BaseModel):
    """Payload for <<plot_point>>"""
    events: List[str]
    precedence: List[str] # Format: "EventA precedes EventB"
    
    event_details: List[GraphNode] = Field(default_factory=list)

class SynthesisOutput(BaseModel):
    """Payload for <<synthesis_output>>"""
    narrative_segment: str

class Feedback(BaseModel):
    """Payload for Critic's evaluation"""
    score: float # 0.0 to 1.0
    critique: str
    suggestion: str
    approved: bool
