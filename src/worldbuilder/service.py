from src.shared.models import StoryRequest, WorldState

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class WorldBuilderService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def update_world(self, request: StoryRequest) -> WorldState:
        # Simple extraction logic
        location_suffix = request.user_input.split()[-1] if request.user_input else "Unknown"
        location_name = f"Forest of {location_suffix}"
        
        # Check if exists
        node_id = f"loc:{location_name.replace(' ', '_').lower()}"
        existing = self.graph_store.get_node(node_id)
        
        if not existing:
            new_node = GraphNode(id=node_id, type="Location", properties={"name": location_name, "description": "A mysterious place."})
            self.graph_store.add_node(new_node)
            
        return WorldState(
            locations=[location_name, "Dragon's Lair"],
            concepts=["Magic", "Bravery"]
        )
