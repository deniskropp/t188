from src.shared.models import StoryRequest, SynthesisOutput
from src.storyteller.service import StorytellerService
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService

class MetaCognito:
    def __init__(self):
        self.storyteller = StorytellerService()
        self.worldbuilder = WorldBuilderService()
        self.charactermanager = CharacterManagerService()
        self.plotweaver = PlotWeaverService()

    async def process_story_request(self, user_input: str) -> SynthesisOutput:
        request = StoryRequest(user_input=user_input)
        
        # 1. Parallel processing of world, characters, and plot
        import asyncio
        world_state, character_update, plot_point = await asyncio.gather(
            self.worldbuilder.update_world(request),
            self.charactermanager.update_characters(request),
            self.plotweaver.weave_plot(request)
        )
        
        # 2. Synthesize the narrative
        result = await self.storyteller.generate_narrative(
            request, 
            plot_point, 
            world_state, 
            character_update
        )
        
        return result
