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

# Subconscious / MindRoles Models

class SubconsciousCue(BaseModel):
    """Data gathered by the Researcher role"""
    cue: str
    context: str

class LatentPattern(BaseModel):
    """Patterns discovered by the Analyst role"""
    pattern: str
    strength: float

class DreamNarrative(BaseModel):
    """Internal summary by the Storyteller role"""
    narrative: str

class ImplicitPlan(BaseModel):
    """Sequenced path by the Planner role"""
    steps: List[str]

class MindState(BaseModel):
    """Composite subconscious state"""
    cues: List[SubconsciousCue] = Field(default_factory=list)
    patterns: List[LatentPattern] = Field(default_factory=list)
    dream: Optional[DreamNarrative] = None
    plan: Optional[ImplicitPlan] = None
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)

# "The Loop" Narrative Engine Models

class JournalEntry(BaseModel):
    """A log of artistic action and psychological reflection."""
    timestamp: float
    action_type: str  # e.g., "stroke", "reflection", "interaction"
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    sentiment: Optional[float] = None  # -1.0 to 1.0

class Badge(BaseModel):
    """A symbol of achievement in the creative loop."""
    id: str
    name: str
    description: str
    icon: str
    earned_at: float

class Quest(BaseModel):
    """A challenge to drive engagement and synchronization."""
    id: str
    title: str
    description: str
    status: str = "active"  # active, completed, claimed
    requirements: Dict[str, Any]
    progress: float = 0.0
    reward_badge_id: Optional[str] = None

class LoopStatus(BaseModel):
    """Real-time neurocognitive state of the collaborative session."""
    dopamine_density: float  # Strokes/minute or recent activity intensity
    flow_time: float        # Duration of uninterrupted deep work
    oxytocin_level: float   # Metric for 'social belonging' or canvas bond
    engagement_index: float # Composite: (Coherence * Resilience * Dopamine) / Drift
    active_quests: List[Quest] = Field(default_factory=list)
    earned_badges: List[Badge] = Field(default_factory=list)
    last_action_at: float
    current_pipes: List[str] = Field(default_factory=list) # "Placebo Pipes" status signals
