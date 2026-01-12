import pytest
from typing import Any, Type
from src.shared.models import StoryRequest, PlotPoint, WorldState, CharacterUpdate, GraphNode
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService
from src.storyteller.service import StorytellerService
from src.shared.graph import GraphStore

class MockLLM:
    async def generate_text(self, prompt: str) -> str:
        return "Mocked narrative segment"

    async def generate_structured(self, prompt: str, schema: Type[Any]) -> Any:
        if "WorldState" in str(schema):
            return WorldState(
                locations=["Forest of Tower"], 
                concepts=[], 
                items=[], 
                nodes=[GraphNode(id="loc:forest_of_tower", type="Location", properties={"name": "Forest of Tower"})], 
                edges=[]
            )
        if "CharacterUpdate" in str(schema):
            return CharacterUpdate(
                characters=["Alice", "Bob"], 
                nodes=[GraphNode(id="char:alice", type="Character", properties={"name": "Alice"})], 
                edges=[]
            )
        if "PlotPoint" in str(schema):
            return PlotPoint(
                events=["Mock Event"], 
                nodes=[GraphNode(id="evt:mock", type="Event", properties={"desc": "Mock"})], 
                edges=[]
            )
        return None

@pytest.mark.asyncio
async def test_worldbuilder_update(graph_store):
    service = WorldBuilderService(graph_store, llm_service=MockLLM())
    req = StoryRequest(user_input="Go to the Dark Tower")
    state = await service.update_world(req)
    assert len(state.locations) > 0
    # verify graph side effect
    assert graph_store.get_node("loc:forest_of_tower") is not None

@pytest.mark.asyncio
async def test_charactermanager_update(graph_store):
    service = CharacterManagerService(graph_store, llm_service=MockLLM())
    req = StoryRequest(user_input="Alice hits Bob")
    update = await service.update_characters(req)
    assert update is not None
    # verify graph side effect
    assert graph_store.get_node("char:alice") is not None

@pytest.mark.asyncio
async def test_plotweaver_weave(graph_store):
    service = PlotWeaverService(graph_store, llm_service=MockLLM())
    req = StoryRequest(user_input="Climax happens")
    plot = await service.weave_plot(req)
    assert plot is not None
    # verify graph side effect
    assert len(graph_store.graph.nodes) > 0 

@pytest.mark.asyncio
async def test_storyteller_generate(graph_store):
    service = StorytellerService(graph_store, llm_service=MockLLM())
    req = StoryRequest(user_input="The end")
    
    res = await service.generate_narrative(
        req, 
        PlotPoint(events=["Something happens"], precedence=[]),
        WorldState(locations=["Void"], concepts=["Nothingness"]),
        CharacterUpdate(characters=["Nobody"], traits=[], interactions=[])
    )
    assert res is not None
    assert isinstance(res.narrative_segment, str)
    assert res.narrative_segment == "Mocked narrative segment"
