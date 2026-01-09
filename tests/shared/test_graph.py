import pytest
from src.shared.models import GraphNode, GraphEdge
from src.shared.graph import GraphStore

def test_graph_node_creation():
    node = GraphNode(id="loc:forest", type="Location", properties={"name": "Dark Forest"})
    assert node.id == "loc:forest"
    assert node.type == "Location"
    assert node.properties["name"] == "Dark Forest"

def test_graph_store_add_get_node(graph_store: GraphStore):
    node = GraphNode(id="char:hero", type="Character", properties={"level": 1})
    graph_store.add_node(node)
    
    retrieved = graph_store.get_node("char:hero")
    assert retrieved is not None
    assert retrieved.id == "char:hero"
    assert retrieved.type == "Character"
    assert retrieved.properties["level"] == 1

def test_graph_store_add_get_edge(graph_store: GraphStore):
    node1 = GraphNode(id="a", type="T")
    node2 = GraphNode(id="b", type="T")
    graph_store.add_node(node1)
    graph_store.add_node(node2)
    
    edge = GraphEdge(source="a", target="b", relationship="connects_to", properties={"weight": 10})
    graph_store.add_edge(edge)
    
    edges = graph_store.get_edges("a")
    assert len(edges) == 1
    assert edges[0].target == "b"
    assert edges[0].relationship == "connects_to"
    assert edges[0].properties["weight"] == 10
