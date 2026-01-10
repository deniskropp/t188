from src.shared.models import StoryRequest, SynthesisOutput, PlotPoint, WorldState, CharacterUpdate
from src.shared.graph import GraphStore

class StorytellerService:
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store

    async def generate_narrative(
        self, 
        request: StoryRequest, 
        plot: PlotPoint, 
        world: WorldState, 
        chars: CharacterUpdate,
        history: list[dict[str, str]] = None
    ) -> SynthesisOutput:
        # Use LLM to generate narrative
        from src.shared.llm import get_llm_service
        from src.shared.config import settings
        
        llm = get_llm_service()
        
        history_text = ""
        if history:
            history_text = "\n".join([f"Turn {i+1}:\nUser: {h['user']}\nStory: {h['story']}" for i, h in enumerate(history)])

        graph_summary = self.graph_store.get_summary()
        
        # Prepare a descriptive prompt for the LLM
        # We use the names from the update objects
        world_desc = ", ".join(world.locations + world.concepts + world.items)
        char_desc = ", ".join(chars.characters)
        plot_desc = "\n".join([f"- {e}" for e in plot.events])
        
        prompt = f"""
        {settings.storyteller_prompt}
        
        Continue the story based on the following updates:
        
        WORLD: {world_desc}
        CHARACTERS: {char_desc}
        PLOT EVENTS:
        {plot_desc}
        
        USER REQUEST: "{request.user_input}"
        
        CURRENT WORLD GRAPH:
        {graph_summary}
        
        NARRATIVE HISTORY:
        {history_text}
        
        Write a coherent and engaging narrative segment that incorporates these elements.
        """
        
        content = await llm.generate_text(prompt)
        return SynthesisOutput(narrative_segment=content)
