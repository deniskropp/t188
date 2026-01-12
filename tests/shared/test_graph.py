import pytest
from src.shared.models import GraphNode, GraphEdge
from src.shared.graph import GraphStore

def test_graph_node_creation():
    node = GraphNode(id="loc:forest", type="Location", properties={"name": "Dark Forest"})
    assert node.id == "loc:forest"
    assert node.type == "Location"
    assert node.properties[0].key == "name"
    assert node.properties[0].value == "Dark Forest"

def test_graph_store_add_get_node(graph_store: GraphStore):
    node = GraphNode(id="char:hero", type="Character", properties={"level": 1})
    graph_store.add_node(node)
    
    retrieved = graph_store.get_node("char:hero")
    assert retrieved is not None
    assert retrieved.id == "char:hero"
    assert retrieved.type == "Character"
    props = {kv.key: kv.value for kv in retrieved.properties}
    assert props["level"] == "1"

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
    edge_props = {kv.key: kv.value for kv in edges[0].properties}
    assert edge_props["weight"] == "10"

def test_graph_store_persistence(graph_store: GraphStore, tmp_path):
    # Setup
    node = GraphNode(id="hero_1", type="Character", properties={"name": "Arthur"})
    graph_store.add_node(node)
    
    file_path = tmp_path / "test_graph.json"
    str_path = str(file_path)
    
    # Save
    graph_store.save_to_json(str_path)
    assert file_path.exists()
    
    # Load into new store
    new_store = GraphStore()
    new_store.load_from_json(str_path)
    
    loaded_node = new_store.get_node("hero_1")
    assert loaded_node is not None
    assert loaded_node.type == "Character"
    props = {kv.key: kv.value for kv in loaded_node.properties}
    assert props["name"] == "Arthur"

