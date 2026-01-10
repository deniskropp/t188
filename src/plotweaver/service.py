from src.shared.models import StoryRequest, PlotPoint

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class PlotWeaverService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def weave_plot(self, request: StoryRequest, context: str = "") -> PlotPoint:
        from src.shared.llm import get_llm_service
        llm = get_llm_service()

        prompt = f"""
        Analyze the following story request and generate a PlotPoint.
        Outline the key events and their precedence/order.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Ensure global plot consistency and progression from previous events.
        If an event already exists or is a continuation, provide updated properties in 'event_details'.
        """
        
        plot_point = await llm.generate_structured(prompt, PlotPoint)
        
        # Sync with Graph
        # First add basic events with stable IDs
        for event in plot_point.events:
             # Create a stable ID based on description
             stable_id = event.replace(" ", "_").lower()[:50]
             event_id = f"evt:{stable_id}"
             if not self.graph_store.get_node(event_id):
                self.graph_store.add_node(GraphNode(
                    id=event_id,
                    type="Event",
                    properties={"description": event, "source": "llm_generated"}
                ))
        
        # Then update with details
        for node in plot_point.event_details:
             self.graph_store.add_node(node)

        return plot_point
