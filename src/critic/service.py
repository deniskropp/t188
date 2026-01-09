from src.shared.models import SynthesisOutput, WorldState, Feedback
from src.shared.config import settings

class CriticService:
    def __init__(self, graph_store):
        # Critic also looks at graph consistency!
        self.graph_store = graph_store

    async def critique(self, narrative: SynthesisOutput, world: WorldState) -> Feedback:
        """
        Evaluates the narrative for quality and consistency.
        """
        from src.shared.llm import GoogleGenAIService
        llm = GoogleGenAIService()
        
        prompt = f"""
        Act as a literary critic and consistency checker.
        Evaluate the following narrative segment against the established world state.
        
        World Context: {world}
        
        Narrative Segment:
        "{narrative.narrative_segment}"
        
        Provide a structured evaluation including a score (0.0-1.0), a critique textual summary,
        a specific suggestion for improvement, and a boolean approval (true if score > {settings.critic_threshold}).
        """
        
        feedback = await llm.generate_structured(prompt, Feedback)
        return feedback
