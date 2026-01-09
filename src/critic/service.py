from src.shared.models import SynthesisOutput, WorldState, Feedback
from src.shared.config import settings

class CriticService:
    def __init__(self, graph_store):
        # Critic also looks at graph consistency!
        self.graph_store = graph_store

    def critique(self, narrative: SynthesisOutput, world: WorldState) -> Feedback:
        """
        Evaluates the narrative for quality and consistency.
        """
        score = 0.8 # Mock score
        approved = True
        critique = "Good flow."
        suggestion = ""
        
        # Simple heuristic: If narrative is too short, reject it.
        if len(narrative.narrative_segment.split()) < 5:
            score = 0.2
            approved = False
            critique = "Too short."
            suggestion = "Expand on the description."
        
        # Check graph consistency (mock)
        # e.g., if narrative mentions a location not in world state?
        
        return Feedback(
            score=score,
            critique=critique,
            suggestion=suggestion,
            approved=approved
        )
