from src.shared.models import StoryRequest, WorldState, GraphNode
from src.shared.base import BaseRole

class WorldBuilderService(BaseRole):
    async def update_world(self, request: StoryRequest, context: str = "") -> WorldState:
        prompt = f"""
        Role: WorldBuilder
        Objective: Maintain the setting, lore, and consistency of the story world.
        
        Analyze the story request and generate a WorldState update.
        Capture new locations, abstract concepts (lore/mythology), and vital physical items.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Instructions:
        1. Maintain strict consistency with established lore and setting.
        2. Identify key locations (e.g. "The Obsidian Citadel").
        3. Extract abstract concepts or lore elements (e.g. "The Rite of Reification").
        4. Detail physical items that have narrative weight.
        5. Ensure nodes have types: "Location", "Concept", or "Item".
        6. Define edges like 'located_in' or 'possesses' to anchor these elements.
        """
        
        world_state = await self._generate_structured(prompt, WorldState)
        
        # Sync with Graph
        self._sync_nodes(world_state.nodes)
             
        # Add basic nodes for any mentioned that don't have full details
        basic_nodes = []
        for loc in world_state.locations:
            node_id = f"loc:{loc.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                basic_nodes.append(GraphNode(id=node_id, type="Location", properties={"name": loc}))

        for concept in world_state.concepts:
            node_id = f"con:{concept.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                basic_nodes.append(GraphNode(id=node_id, type="Concept", properties={"name": concept}))
        
        for item in world_state.items:
            node_id = f"itm:{item.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                basic_nodes.append(GraphNode(id=node_id, type="Item", properties={"name": item}))

        self._sync_nodes(basic_nodes)
        self._sync_edges(world_state.edges)
                
        return world_state
