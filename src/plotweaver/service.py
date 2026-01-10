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
        
        - events: Short descriptions of events.
        - nodes: Full details for events. Type must be "Event".
        - edges: Relationships like 'precedes' between events.
        """
        
        plot_point = await llm.generate_structured(prompt, PlotPoint)
        
        # Sync with Graph
        # Add or update nodes
        for node in plot_point.nodes:
             self.graph_store.add_node(node)
             
        # Add basic events if details missing
        for event in plot_point.events:
             stable_id = event.replace(" ", "_").lower()[:50]
             event_id = f"evt:{stable_id}"
             if not self.graph_store.get_node(event_id):
                self.graph_store.add_node(GraphNode(id=event_id, type="Event", properties={"description": event}))
        
        # Sync edges
        for edge in plot_point.edges:
             self.graph_store.add_edge(edge)

        return plot_point
