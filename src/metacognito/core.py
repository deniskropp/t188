from src.shared.models import StoryRequest, SynthesisOutput
from src.storyteller.service import StorytellerService
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService

from src.shared.graph import GraphStore

from src.shared.pipes import Pipe
from src.shared.models import WorldState, CharacterUpdate, PlotPoint

from src.metacognito.resolver import ConflictResolver
from src.critic.service import CriticService
from src.shared.config import settings

class MetaCognito:
    def __init__(self):
        self.graph_store = GraphStore()
        self.storyteller = StorytellerService(self.graph_store)
        self.worldbuilder = WorldBuilderService(self.graph_store)
        self.charactermanager = CharacterManagerService(self.graph_store)
        self.plotweaver = PlotWeaverService(self.graph_store)
        self.resolver = ConflictResolver()
        self.critic = CriticService(self.graph_store)

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
        
        # 4. Refinement Loop
        approved = False
        attempt = 0
        current_directive = directive
        
        result = None
        
        while not approved and attempt < settings.max_refinement_steps:
            attempt += 1
            
            # Pass (potentially updated) directive/context to storyteller
            # (Note: Prototype Storyteller doesn't use directive arg yet, but we logically track it)
            result = await self.storyteller.generate_narrative(
                request, 
                p_data, 
                w_data, 
                c_data
            )
            
            if "CONFLICT" in current_directive:
                 result.narrative_segment += f"\n[System Note: {current_directive}]"
            
            # Critique
            feedback = self.critic.critique(result, w_data)
            
            if feedback.approved:
                approved = True
                # Log success
                # print(f"Approved on attempt {attempt}")
            else:
                # Feedback loop: Update directive/request for next try
                current_directive += f" CRITIC: {feedback.suggestion}"
                # In real LLM impl, we'd pass previous output + critique
                
                # Mock "improvement": Append something to reach length requirement if that was the fail reason
                if "Expand" in feedback.suggestion:
                    # Mocking the LLM listening to feedback
                    # "We force the next generation to be different"
                    pass # In this mock, Storyteller is deterministic, so it might fail forever.
                         # We need Storyteller to be slightly adaptable or Mock logic to handle 'retry'.
        
        if not approved:
            result.narrative_segment += "\n[Warning: Critic usage limit reached. Output may be unrefined.]"

        return result
