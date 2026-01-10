from src.shared.models import StoryRequest, CharacterUpdate, GraphNode
from src.shared.base import BaseRole

class CharacterManagerService(BaseRole):
    async def update_characters(self, request: StoryRequest, context: str = "") -> CharacterUpdate:
        prompt = f"""
        Role: CharacterManager
        Objective: Track character arcs, traits, and dialogue dynamics through relations.
        
        Analyze the story request and generate a CharacterUpdate.
        Focus on characters' evolution, their internal traits, and evolving relationships.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Instructions:
        1. Identify characters and their current state/arc progression.
        2. Assign descriptive traits using 'has_trait' edge relations.
        3. Define dialogue or social dynamics via 'interacts_with' or 'influenced_by'.
        4. Track possession of items via 'possesses' (linking to World Items).
        5. Node type must be "Character".
        """
        
        char_update = await self._generate_structured(prompt, CharacterUpdate)
        
        # Sync with Graph
        self._sync_nodes(char_update.nodes)
        
        # Add basic characters if details missing
        basic_nodes = []
        for char_name in char_update.characters:
            node_id = f"char:{char_name.lower()}"
            if not self.graph_store.get_node(node_id):
                basic_nodes.append(GraphNode(id=node_id, type="Character", properties={"name": char_name}))

        self._sync_nodes(basic_nodes)
        self._sync_edges(char_update.edges)
        
        return char_update
