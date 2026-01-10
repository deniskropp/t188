import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.metacognito.core import MetaCognito
from src.shared.models import (
    WorldState, CharacterUpdate, PlotPoint, 
    GraphNode, GraphEdge, KeyValue, Feedback
)

@pytest.mark.asyncio
async def test_storybook_objective_compliance():
    """
    Verify that the system creates the required node and edge types
    as specified in the Meta-AI Storybook Objective.
    """
    with patch("src.shared.llm.MistralService") as MockService:
        mock_llm = AsyncMock()
        MockService.return_value = mock_llm
        
        # 1. Mock the responses to include specific nodes and edges
        node_char = GraphNode(id="char:jax", type="Character", properties=[KeyValue(key="name", value="Jax")])
        node_loc = GraphNode(id="loc:temple", type="Location", properties=[KeyValue(key="name", value="Temple")])
        node_itm = GraphNode(id="itm:gem", type="Item", properties=[KeyValue(key="name", value="Magic Gem")])
        node_evt = GraphNode(id="evt:theft", type="Event", properties=[KeyValue(key="description", value="The Gem was stolen")])
        node_con = GraphNode(id="con:prophecy", type="Concept", properties=[KeyValue(key="name", value="Prophecy")])

        edge_trait = GraphEdge(source="char:jax", target="trait:thief", relationship="has_trait")
        edge_loc = GraphEdge(source="itm:gem", target="loc:temple", relationship="located_in")
        edge_interact = GraphEdge(source="char:jax", target="char:thorne", relationship="interacts_with")
        edge_possess = GraphEdge(source="char:jax", target="itm:gem", relationship="possesses")
        edge_precede = GraphEdge(source="evt:theft", target="evt:chase", relationship="precedes")

        mock_llm.generate_structured.side_effect = [
            WorldState(locations=["Temple"], concepts=["Prophecy"], items=["Magic Gem"], nodes=[node_loc, node_con, node_itm], edges=[edge_loc]),
            CharacterUpdate(characters=["Jax", "Thorne"], nodes=[node_char], edges=[edge_trait, edge_interact, edge_possess]),
            PlotPoint(events=["Theft", "Chase"], nodes=[node_evt], edges=[edge_precede]),
            Feedback(score=1.0, critique="Perfect", suggestion="", approved=True)
        ]
        mock_llm.generate_text.return_value = "Jax stole the gem from the temple."

        system = MetaCognito()
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
