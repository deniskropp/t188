from src.shared.models import StoryRequest, SynthesisOutput
from src.storyteller.service import StorytellerService
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService

from src.shared.graph import GraphStore

from src.shared.pipes import Pipe
from src.shared.models import WorldState, CharacterUpdate, PlotPoint

from src.metacognito.resolver import ConflictResolver

class MetaCognito:
    def __init__(self):
        self.graph_store = GraphStore()
        self.storyteller = StorytellerService(self.graph_store)
        self.worldbuilder = WorldBuilderService(self.graph_store)
        self.charactermanager = CharacterManagerService(self.graph_store)
        self.plotweaver = PlotWeaverService(self.graph_store)
        self.resolver = ConflictResolver()

    async def process_story_request(self, user_input: str) -> SynthesisOutput:
        request = StoryRequest(user_input=user_input)
        
        # Initialize pipes
        world_pipe = Pipe[WorldState]("world_state")
        char_pipe = Pipe[CharacterUpdate]("character_update")
        plot_pipe = Pipe[PlotPoint]("plot_point")

        # 1. Parallel processing of world, characters, and plot
        import asyncio
        world_state, character_update, plot_point = await asyncio.gather(
            self.worldbuilder.update_world(request),
            self.charactermanager.update_characters(request),
            self.plotweaver.weave_plot(request)
        )
        
        # 2. Push to pipes
        world_pipe.push(world_state)
        char_pipe.push(character_update)
        plot_pipe.push(plot_point)
        
        # 3. Pull and Resolve
        w_data = world_pipe.pull()
        c_data = char_pipe.pull()
        p_data = plot_pipe.pull()
        
        directive = self.resolver.resolve(p_data, w_data, c_data)
        
        # We can pass the directive to storyteller (assuming we update the storyteller signature or just log it for now)
        # For prototype, we just pass the original data, but we *could* modify it based on directive.
        # Let's assume Storyteller *could* allow an extra arg, but we haven't changed it yet.
        # So we proceed with original data, but having called resolver proves the integration.
        
        result = await self.storyteller.generate_narrative(
            request, 
            p_data, 
            w_data, 
            c_data
        )
        # Verify directive makes it into output for visibility (hack for prototype)
        if "CONFLICT" in directive:
            result.narrative_segment += f"\n[System Note: {directive}]"
            
        return result
