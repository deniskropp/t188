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
        Identify the main characters, their traits, and initial interaction dynamics.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Maintain consistency with existing characters and their traits.
        """
        
        char_update = await llm.generate_structured(prompt, CharacterUpdate)
        
        # Sync with Graph
        for char_name in char_update.characters:
            node_id = f"char:{char_name.lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(
                    id=node_id, 
                    type="Character", 
                    properties={"name": char_name, "source": "llm_generated"}
                ))
        
        return char_update
