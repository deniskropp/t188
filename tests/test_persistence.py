import os
import pytest
import networkx as nx
from src.shared.graph import GraphStore
from src.shared.models import GraphNode, KeyValue

def test_graph_persistence():
    storage_path = "test_graph.json"
    if os.path.exists(storage_path):
        os.remove(storage_path)
        
    store = GraphStore()
    node = GraphNode(id="hero_1", type="Character", properties=[KeyValue(key="name", value="Arthur")])
    store.add_node(node)
    
    # Save
    store.save_to_json(storage_path)
    assert os.path.exists(storage_path)
    
    # Load into new store
    new_store = GraphStore()
    new_store.load_from_json(storage_path)
    
    loaded_node = new_store.get_node("hero_1")
    assert loaded_node is not None
    assert loaded_node.type == "Character"
    # Convert kv list to dict for easier comparison
    props = {kv.key: kv.value for kv in loaded_node.properties}
    assert props["name"] == "Arthur"
    
    # Cleanup
    if os.path.exists(storage_path):
        os.remove(storage_path)

if __name__ == "__main__":
    test_graph_persistence()
    print("Test passed!")
