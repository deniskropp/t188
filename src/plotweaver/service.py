from src.shared.models import StoryRequest, PlotPoint

from src.shared.graph import GraphStore
from src.shared.models import GraphNode

class PlotWeaverService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def weave_plot(self, request: StoryRequest, context: str = "") -> PlotPoint:
        from src.shared.llm import GoogleGenAIService
        llm = GoogleGenAIService()

        prompt = f"""
        Analyze the following story request and generate a PlotPoint.
        Outline the key events and their precedence/order.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Ensure global plot consistency and progression from previous events.
        """
        
        plot_point = await llm.generate_structured(prompt, PlotPoint)
        
        # Sync with Graph
        for event in plot_point.events:
             event_id = f"evt:{hash(event)}"
             if not self.graph_store.get_node(event_id):
                self.graph_store.add_node(GraphNode(
                    id=event_id,
                    type="Event",
                    properties={"description": event, "source": "llm_generated"}
                ))

        return plot_point
