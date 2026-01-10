from src.shared.models import StoryRequest, CharacterUpdate

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class CharacterManagerService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def update_characters(self, request: StoryRequest, context: str = "") -> CharacterUpdate:
        from src.shared.llm import get_llm_service
        llm = get_llm_service()
        
        prompt = f"""
        Analyze the following story request and generate a CharacterUpdate.
        Identify the characters involved, their traits, and relationships.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        - characters: names of characters
        - nodes: Full details for characters. Type must be "Character".
        - edges: Relationships like 'has_trait', 'interacts_with', or 'possesses' (for Items).
        """
        
        char_update = await llm.generate_structured(prompt, CharacterUpdate)
        
        # Sync with Graph
        # Add or update nodes
        for node in char_update.nodes:
             self.graph_store.add_node(node)
        
        # Add basic characters if details missing
        for char_name in char_update.characters:
            node_id = f"char:{char_name.lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(id=node_id, type="Character", properties={"name": char_name}))

        # Sync edges
        for edge in char_update.edges:
            self.graph_store.add_edge(edge)
        
        return char_update
