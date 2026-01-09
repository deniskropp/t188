from src.shared.models import StoryRequest, CharacterUpdate

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class CharacterManagerService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def update_characters(self, request: StoryRequest) -> CharacterUpdate:
        # Simple heuristic: treat capitalized words as potential characters
        potential_chars = [w for w in request.user_input.split() if w[0].isupper()]
        characters = potential_chars if potential_chars else ["Hero", "Dragon"]
        
        for char_name in characters:
            node_id = f"char:{char_name.lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(
                    id=node_id, 
                    type="Character", 
                    properties={"name": char_name, "role": "Protagonist" if char_name == "Hero" else "Antagonist"}
                ))
        
        return CharacterUpdate(
            characters=characters,
            traits=["brave", "fierce"],
            interactions=[f"{characters[0]} interacts_with {characters[-1] if len(characters) > 1 else 'Self'}"]
        )
