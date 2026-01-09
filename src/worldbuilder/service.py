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
        Identify key locations and abstract concepts that set the scene.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Maintain consistency with existing locations and concepts if they are relevant.
        """
        
        world_state = await llm.generate_structured(prompt, WorldState)
        
        # Sync with Graph
        for location in world_state.locations:
            node_id = f"loc:{location.replace(' ', '_').lower()}"
            if not self.graph_store.get_node(node_id):
                self.graph_store.add_node(GraphNode(
                    id=node_id, 
                    type="Location", 
                    properties={"name": location, "source": "llm_generated"}
                ))
                
        return world_state
