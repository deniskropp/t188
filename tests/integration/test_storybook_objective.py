import pytest
from src.metacognito.core import MetaCognito
from src.shared.models import (
    WorldState, CharacterUpdate, PlotPoint, 
    GraphNode, GraphEdge, KeyValue, Feedback
)
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_storybook_objective_compliance(mock_llm_service):
    """
    Verify that the system creates the required node and edge types
    as specified in the Meta-AI Storybook Objective.
    """
    # 1. Configure the mock to return specific nodes/edges for this test
    # We need to preserve the ability to return CueList etc for Planner phases if needed,
    # or just Mock everything if Planner is skipped or handled.
    # Planner WILL be called. So we need to handle CueList etc. or let default MockLLM handle them.
    # We can wrap the default method.
    
    original_generate = mock_llm_service.generate_structured
    
    async def custom_structured(prompt, schema):
        schema_name = schema.__name__
        
        # Override for Core Pipeline to match Objective requirements
        if schema_name == "WorldState":
            node_loc = GraphNode(id="loc:temple", type="Location", properties=[KeyValue(key="name", value="Temple")])
            node_itm = GraphNode(id="itm:gem", type="Item", properties=[KeyValue(key="name", value="Magic Gem")])
            node_con = GraphNode(id="con:prophecy", type="Concept", properties=[KeyValue(key="name", value="Prophecy")])
            edge_loc = GraphEdge(source="itm:gem", target="loc:temple", relationship="located_in")
            return WorldState(locations=["Temple"], concepts=["Prophecy"], items=["Magic Gem"], nodes=[node_loc, node_con, node_itm], edges=[edge_loc])
            
        if schema_name == "CharacterUpdate":
            node_char = GraphNode(id="char:jax", type="Character", properties=[KeyValue(key="name", value="Jax")])
            edge_trait = GraphEdge(source="char:jax", target="trait:thief", relationship="has_trait")
            edge_interact = GraphEdge(source="char:jax", target="char:thorne", relationship="interacts_with")
            edge_possess = GraphEdge(source="char:jax", target="itm:gem", relationship="possesses")
            return CharacterUpdate(characters=["Jax", "Thorne"], nodes=[node_char], edges=[edge_trait, edge_interact, edge_possess])
            
        if schema_name == "PlotPoint":
            node_evt = GraphNode(id="evt:theft", type="Event", properties=[KeyValue(key="description", value="The Gem was stolen")])
            edge_precede = GraphEdge(source="evt:theft", target="evt:chase", relationship="precedes")
            return PlotPoint(events=["Theft", "Chase"], nodes=[node_evt], edges=[edge_precede])
        
        # Fallback to original for Planner types (CueList, etc)
        return await original_generate(prompt, schema)

    mock_llm_service.generate_structured = custom_structured
    mock_llm_service.generate_text = MagicMock(return_value="Jax stole the gem from the temple.") # async mock needed? generate_text is async
    async def mock_text(prompt): return "Jax stole the gem from the temple."
    mock_llm_service.generate_text = mock_text

    system = MetaCognito()
    # Ensure graph is clear
    system.graph_store.clear()
    
    # 2. Run the request
    await system.process_story_request("Jax steals the gem from the temple")
    
    # 3. Verify Graph State
    graph = system.graph_store.graph
    
    # Check Node Types
    node_types = {data.get('type') for _, data in graph.nodes(data=True)}
    assert "Character" in node_types
    assert "Location" in node_types
    assert "Event" in node_types
    assert "Item" in node_types
    assert "Concept" in node_types
    
    # Check Edges (Relationships)
    edges = []
    for u, v, key, data in graph.edges(keys=True, data=True):
        edges.append(key)
        
    assert "has_trait" in edges
    assert "located_in" in edges
    assert "interacts_with" in edges
    assert "possesses" in edges
    assert "precedes" in edges
    
    print("\nStorybook Objective Verification: SUCCESS")
