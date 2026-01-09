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
        chars: CharacterUpdate
    ) -> SynthesisOutput:
        # In a real implementation, this would use an LLM or logic to weave the inputs
        narrative = (
            f"The story begins in the {world.locations[0]}. "
            f"{chars.characters[0]} stands ready. "
            f"Suddenly, {plot.events[0]}. "
            f"The world reacts: {world.concepts[0]} fills the air."
        )
        return SynthesisOutput(narrative_segment=narrative)
