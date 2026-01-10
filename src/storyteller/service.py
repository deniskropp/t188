from src.shared.models import StoryRequest, SynthesisOutput, PlotPoint, WorldState, CharacterUpdate
from src.shared.base import BaseRole

class StorytellerService(BaseRole):
    async def generate_narrative(
        self, 
        request: StoryRequest, 
        plot: PlotPoint, 
        world: WorldState, 
        chars: CharacterUpdate,
        history: list[dict[str, str]] = None
    ) -> SynthesisOutput:
        from src.shared.config import settings
        
        history_text = ""
        if history:
            history_text = "\n".join([f"Turn {i+1}:\nUser: {h['user']}\nStory: {h['story']}" for i, h in enumerate(history)])

        graph_summary = self.graph_store.get_summary()
        
        # Prepare a descriptive prompt for the LLM
        world_desc = ", ".join(world.locations + world.concepts + world.items)
        char_desc = ", ".join(chars.characters)
        plot_desc = "\n".join([f"- {e}" for e in plot.events])
        
        prompt = f"""
        Role: Storyteller
        Objective: Generate immersive narrative content explicitly derived from graph elements.
        
        {settings.storyteller_prompt}
        
        Continue the story based on the following specific updates and the current World Graph state.
        Your primary goal is to weave the established Lore, Character Traits, and Plot Events into the prose.
        
        ---
        UPDATES FROM CORE ROLES:
        World (Lore/Setting): {world_desc}
        Characters (Arcs/Traits): {char_desc}
        Plot (Conflict/Events): 
        {plot_desc}
        ---
        
        USER REQUEST: "{request.user_input}"
        
        CURRENT WORLD GRAPH (Lore & Relationships):
        {graph_summary}
        
        NARRATIVE HISTORY:
        {history_text}
        
        Instructions:
        1. Explicitly reference locations and lore concepts provided in the World updates.
        2. Highlight character traits and relationship dynamics from the Character updates.
        3. Enact the conflict-driven events sequenced by the Plot updates.
        4. Ensure the narrative flows naturally from the history while strictly adhering to the new graph data.
        """
        
        content = await self._generate_text(prompt)
        return SynthesisOutput(narrative_segment=content)
