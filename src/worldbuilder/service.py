from src.shared.models import StoryRequest, WorldState

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class WorldBuilderService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def update_world(self, request: StoryRequest, context: str = "") -> WorldState:
        from src.shared.llm import get_llm_service
        llm = get_llm_service()
        
        prompt = f"""
        Analyze the following story request and generate a rich WorldState.
        Identify key locations, abstract concepts (lore), and physical items.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Maintain consistency with existing elements.
        - locations: name of locations (e.g. "The Dark Forest")
        - concepts: abstract ideas or lore elements (e.g. "The Prophecy of Shadows")
        - items: physical objects (e.g. "The Silver Key")
        - nodes: Full details for these nodes. Ensure types are "Location", "Concept", or "Item".
        - edges: Relationships like 'located_in' (Item/Location -> Location) or 'possesses'.
        """
        
        world_state = await llm.generate_structured(prompt, WorldState)
        
        # Sync with Graph
        # Add or update nodes
        for node in world_state.nodes:
             self.graph_store.add_node(node)
             
        # Add basic nodes for any mentioned that don't have full details
        for loc in world_state.locations:
            node_id = f"loc:{loc.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(id=node_id, type="Location", properties={"name": loc}))

        for concept in world_state.concepts:
            node_id = f"con:{concept.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(id=node_id, type="Concept", properties={"name": concept}))
        
        for item in world_state.items:
            node_id = f"itm:{item.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(id=node_id, type="Item", properties={"name": item}))

        # Sync edges
        for edge in world_state.edges:
            self.graph_store.add_edge(edge)
                
        return world_state
