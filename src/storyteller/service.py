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
        from src.shared.llm import GoogleGenAIService
        from src.shared.config import settings
        
        llm = GoogleGenAIService()
        
        history_text = ""
        if history:
            history_text = "\n".join([f"Turn {i+1}:\nUser: {h['user']}\nStory: {h['story']}" for i, h in enumerate(history)])

        graph_summary = self.graph_store.get_summary()
        
        context_prompt = f"""
        {settings.storyteller_prompt}
        
        Write the next segment of the story based on these inputs.
        
        CURRENT WORLD GRAPH:
        {graph_summary}
        
        NARRATIVE HISTORY:
        {history_text}
        
        NEW INPUTS FOR THIS TURN:
        Request: {request.user_input}
        
        World State Updates:
        - Locations: {', '.join(world.locations)}
        - Concepts: {', '.join(world.concepts)}
        
        Character Updates:
        - Present: {', '.join(chars.characters)}
        - Interactions: {', '.join(chars.interactions)}
        
        Plot Event Updates:
        - Events: {', '.join(plot.events)}
        - Plan: {', '.join(plot.precedence)}
        """
        
        narrative_text = await llm.generate_text(context_prompt)
        
        return SynthesisOutput(narrative_segment=narrative_text)
