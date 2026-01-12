import pytest
import asyncio
from typing import Any, Type
from src.shared.graph import GraphStore
from src.shared.models import (
    WorldState, CharacterUpdate, PlotPoint, Feedback, 
    GraphNode, GraphEdge, KeyValue, ImplicitPlan, DreamNarrative, MindState
)

# Try imports for planner internal models, handle if they don't exist yet
try:
    from src.planner.service import CueList, PatternList
except ImportError:
    CueList = None
    PatternList = None

from src.shared.models import SubconsciousCue, LatentPattern

class MockLLM:
    async def generate_text(self, prompt: str) -> str:
        return "Mocked narrative segment"

    async def generate_structured(self, prompt: str, schema: Type[Any]) -> Any:
        schema_name = schema.__name__
        
        if schema_name == "WorldState":
            return WorldState(
                locations=["Mock Location"], 
                concepts=[], 
                items=[], 
                nodes=[GraphNode(id="loc:mock", type="Location", properties={"name": "Mock Location"})], 
                edges=[]
            )
        if schema_name == "CharacterUpdate":
            return CharacterUpdate(
                characters=["Alice", "Bob"], 
                nodes=[GraphNode(id="char:alice", type="Character", properties={"name": "Alice"})], 
                edges=[]
            )
        if schema_name == "PlotPoint":
            return PlotPoint(
                events=["Mock Event"], 
                nodes=[GraphNode(id="evt:mock", type="Event", properties={"desc": "Mock"})], 
                edges=[]
            )
        if schema_name == "Feedback": # for Critic
            return Feedback(score=1.0, critique="Good", suggestion="None", approved=True)
        
        if schema_name == "MindState":
             return MindState(cues=[], patterns=[], dream=None, plan=None)

        if schema_name == "ImplicitPlan":
            return ImplicitPlan(steps=["Step 1", "Step 2"])
            
        if schema_name == "DreamNarrative":
             return DreamNarrative(narrative="Mock Dream")
             
        if schema_name == "CueList" and CueList:
            return CueList(cues=[SubconsciousCue(cue="Mock Cue", context="Context")])
            
        if schema_name == "PatternList" and PatternList:
            return PatternList(patterns=[LatentPattern(pattern="Mock Pattern", strength=0.8)])

        # Fallback for generics or unknown schemas if possible, or return None causing error
        # Assuming we covered all basics. 
        # For integration tests checking specific values, we might need more logic or side_effect overrides
        return None

@pytest.fixture(scope="function")
def graph_store():
    store = GraphStore()
    yield store
    store.clear()

@pytest.fixture
def mock_llm_service(monkeypatch):
    mock = MockLLM()
    # Patch in both locations to be safe
    monkeypatch.setattr("src.shared.base.get_llm_service", lambda: mock)
    monkeypatch.setattr("src.shared.llm.get_llm_service", lambda: mock)
    return mock

