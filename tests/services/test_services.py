import pytest
from src.shared.models import StoryRequest, PlotPoint, WorldState, CharacterUpdate
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService
from src.storyteller.service import StorytellerService
from src.shared.graph import GraphStore

@pytest.mark.asyncio
async def test_worldbuilder_update(graph_store):
    service = WorldBuilderService(graph_store)
    req = StoryRequest(user_input="Go to the Dark Tower")
    state = await service.update_world(req)
    assert len(state.locations) > 0
    # verify graph side effect
    assert graph_store.get_node("loc:forest_of_tower") is not None

@pytest.mark.asyncio
async def test_charactermanager_update(graph_store):
    service = CharacterManagerService(graph_store)
    req = StoryRequest(user_input="Alice hits Bob")
    update = await service.update_characters(req)
    assert update is not None
    # verify graph side effect
    assert graph_store.get_node("char:alice") is not None

@pytest.mark.asyncio
async def test_plotweaver_weave(graph_store):
    service = PlotWeaverService(graph_store)
    req = StoryRequest(user_input="Climax happens")
    plot = await service.weave_plot(req)
    assert plot is not None
    # verify graph side effect
    assert len(graph_store.graph.nodes) > 0 # minimal check for event

@pytest.mark.asyncio
async def test_storyteller_generate(graph_store):
    service = StorytellerService(graph_store)
    req = StoryRequest(user_input="The end")
    # We need mock inputs for plot, world, char
    # Constructing minimal mocks
    from src.shared.models import PlotPoint, WorldState, CharacterUpdate
    
    # Assuming the method signature: generate_narrative(request, plot_point, world_state, character_update)
    # We can pass None if the service handles it, or empty objects.
    # Let's pass empty objects to be safe.
    res = await service.generate_narrative(
        req, 
        PlotPoint(events=["Something happens"], precedence=[]),
        WorldState(locations=["Void"], concepts=["Nothingness"]),
        CharacterUpdate(characters=["Nobody"], traits=[], interactions=[])
    )
    assert res is not None
    assert isinstance(res.narrative_segment, str)
