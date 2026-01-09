from src.shared.models import StoryRequest, SynthesisOutput
from src.storyteller.service import StorytellerService
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService

from src.shared.graph import GraphStore

from src.shared.pipes import Pipe
from src.shared.models import WorldState, CharacterUpdate, PlotPoint

class MetaCognito:
    def __init__(self):
        self.graph_store = GraphStore()
        self.storyteller = StorytellerService(self.graph_store)
        self.worldbuilder = WorldBuilderService(self.graph_store)
        self.charactermanager = CharacterManagerService(self.graph_store)
        self.plotweaver = PlotWeaverService(self.graph_store)

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
        
        # 3. Pull from pipes for synthesis
        # In a real async/event-driven system, these might be handled by separate consumers.
        # Here we simulate the "flow" by pulling immediately.
        result = await self.storyteller.generate_narrative(
            request, 
            plot_pipe.pull(), 
            world_pipe.pull(), 
            char_pipe.pull()
        )
        
        return result
