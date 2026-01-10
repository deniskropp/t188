from src.shared.models import StoryRequest, PlotPoint, GraphNode
from src.shared.base import BaseRole

class PlotWeaverService(BaseRole):
    async def weave_plot(self, request: StoryRequest, context: str = "") -> PlotPoint:
        prompt = f"""
        Role: PlotWeaver
        Objective: Advance conflict and narrative progression through event sequencing.
        
        Analyze the story request and generate a PlotPoint update.
        Outline key events, ensuring they drive the story forward and introduce or escalate conflicts.
        
        Existing Context:
        {context}
        
        New Request: "{request.user_input}"
        
        Instructions:
        1. Identify pivotal events that advance the plot.
        2. Ensure events have a clear sequence using 'precedes' relations.
        3. Prioritize events that highlight conflict and stakes.
        4. Node type must be "Event".
        5. Consistency with World and Character states is paramount.
        """
        
        plot_point = await self._generate_structured(prompt, PlotPoint)
        
        # Sync with Graph
        self._sync_nodes(plot_point.nodes)
             
        # Add basic events if details missing
        basic_nodes = []
        for event in plot_point.events:
             stable_id = event.replace(" ", "_").lower()[:50]
             event_id = f"evt:{stable_id}"
             if not self.graph_store.get_node(event_id):
                basic_nodes.append(GraphNode(id=event_id, type="Event", properties={"description": event}))
        
        self._sync_nodes(basic_nodes)
        self._sync_edges(plot_point.edges)

        return plot_point
