from src.shared.models import StoryRequest, PlotPoint

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class PlotWeaverService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def weave_plot(self, request: StoryRequest) -> PlotPoint:
        event_desc = f"Action triggered by '{request.user_input[:20]}...'"
        event_id = f"evt:{hash(event_desc)}"
        
        if not self.graph_store.get_node(event_id):
            self.graph_store.add_node(GraphNode(
                id=event_id,
                type="Event",
                properties={"description": event_desc}
            ))

        return PlotPoint(
            events=[event_desc, "Consequence unfolds"],
            precedence=["Action precedes Consequence"]
        )
