from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Base Graph Elements
class GraphNode(BaseModel):
    id: str
    type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str
    properties: Dict[str, Any] = Field(default_factory=dict)

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
