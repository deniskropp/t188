from typing import Optional, Callable
from src.shared.models import StoryRequest, SynthesisOutput
from src.storyteller.service import StorytellerService
from src.worldbuilder.service import WorldBuilderService
from src.charactermanager.service import CharacterManagerService
from src.plotweaver.service import PlotWeaverService

from src.shared.graph import GraphStore

from src.shared.pipes import Pipe
from src.shared.models import WorldState, CharacterUpdate, PlotPoint, MindState

from src.metacognito.resolver import ConflictResolver
from src.critic.service import CriticService
from src.shared.config import settings

from src.planner.orchestrator import MetaCognitoPlanner
from src.planner.memory import StorytellerPlannerMemory

class MetaCognito:
    def __init__(self):
        self.graph_store = GraphStore()
        self.storyteller = StorytellerService(self.graph_store)
        self.worldbuilder = WorldBuilderService(self.graph_store)
        self.charactermanager = CharacterManagerService(self.graph_store)
        self.plotweaver = PlotWeaverService(self.graph_store)
        self.resolver = ConflictResolver()
        self.critic = CriticService(self.graph_store)
        self.planner = MetaCognitoPlanner(self.graph_store)
        self.history = []
        self._load_state()

    def _load_state(self):
        self.graph_store.load_from_json(settings.graph_storage_path)
        import json
        import os
        h_path = settings.graph_storage_path.replace(".json", "_history.json")
        if os.path.exists(h_path):
            with open(h_path, "r") as f:
                self.history = json.load(f)

    def _save_state(self):
        self.graph_store.save_to_json(settings.graph_storage_path)
        import json
        h_path = settings.graph_storage_path.replace(".json", "_history.json")
        with open(h_path, "w") as f:
            json.dump(self.history, f, indent=2)

    def reset(self):
        self.graph_store.clear()
        self.history = []
        import os
        h_path = settings.graph_storage_path.replace(".json", "_history.json")
        if os.path.exists(h_path):
            os.remove(h_path)
        if os.path.exists(settings.graph_storage_path):
            os.remove(settings.graph_storage_path)

    async def _get_context(self) -> str:
        graph_summary = self.graph_store.get_summary()
        history_summary = "\n".join([f"Q: {h['user']} A: {str(h["story"])[:100]}..." for h in self.history])
        return f"GRAPH SUMMARY:\n{graph_summary}\nHISTORY:\n{history_summary}"

    async def process_story_request(self, user_input: str, callback: Optional[Callable] = None, mind_state: Optional[MindState] = None) -> SynthesisOutput:
        request = StoryRequest(user_input=user_input)
        
        # Initialize pipes
        world_pipe = Pipe[WorldState]("world_state")
        char_pipe = Pipe[CharacterUpdate]("character_update")
        plot_pipe = Pipe[PlotPoint]("plot_point")

        # Prepare Context
        context = await self._get_context()

        if not mind_state:
            if callback:
                await callback("KickLang Operation: Planning", "Invoking Subconscious Planner...")
            # 0. Subconscious Planning
            mind_state = await self.planner.plan_pipeline(request, context=context, callback=callback)
        else:
            if callback:
                await callback("KickLang Operation: Context", "Using existing subconscious plan.")
        subconscious_synthesis = StorytellerPlannerMemory.compile_synthesis(mind_state)
        
        if callback:
             await callback("Subconscious Output", subconscious_synthesis)
             await callback("KickLang Operation: Planning", "Invoking WorldBuilder, CharacterManager, and PlotWeaver...")

        # 1. Parallel processing of world, characters, and plot
        import asyncio
        world_state, character_update, plot_point = await asyncio.gather(
            self.worldbuilder.update_world(request, context=context),
            self.charactermanager.update_characters(request, context=context),
            self.plotweaver.weave_plot(request, context=context)
        )
        
        if callback:
             await callback("KickLang Operation: Coordination", "Synchronizing graph updates through Placebo Pipes.")

        # 2. Push to pipes
        world_pipe.push(world_state)
        char_pipe.push(character_update)
        plot_pipe.push(plot_point)
        
        # 3. Pull and Resolve
        w_data = world_pipe.pull()
        c_data = char_pipe.pull()
        p_data = plot_pipe.pull()
        
        directive = self.resolver.resolve(p_data, w_data, c_data)
        
        if callback:
             await callback("KickLang Operation: Synthesis", "Storyteller is deriving narrative from graph state...")

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
                c_data,
                history=self.history
            )
            
            if "CONFLICT" in current_directive:
                 result.narrative_segment += f"\n[System Note: {current_directive}]"
            
            # Critique
            feedback = await self.critic.critique(result, w_data)
            
            if feedback.approved:
                approved = True
            else:
                if callback:
                    await callback("Refinement", f"Critic suggested refinement: {feedback.suggestion}")
                current_directive += f" CRITIC: {feedback.suggestion}"
        
        if not approved:
            result.narrative_segment += "\n[Warning: Critic usage limit reached. Output may be unrefined.]"

        if callback:
             await callback("Finalizing", "Updating Knowledge Graph and history...")

        # Update Session History
        self.history.append({
            "user": user_input,
            "story": result.narrative_segment
        })

        # Persist everything
        self._save_state()

        return result

    async def transform_state(self, user_input: str, callback: Optional[Callable] = None):
        """
        Processes a transformation request to update the Knowledge Graph without generating a narrative.
        """
        request = StoryRequest(user_input=user_input)
        
        # Prepare Context
        graph_summary = self.graph_store.get_summary()
        history_summary = "\n".join([f"Q: {h['user']} A: {str(h["story"])[:100]}..." for h in self.history])
        context = f"GRAPH SUMMARY:\n{graph_summary}\nHISTORY:\n{history_summary}"

        if callback:
            await callback("Transforming", "Agents are analyzing the state change...")

        # 1. Parallel processing of world, characters, and plot
        import asyncio
        world_state, character_update, plot_point = await asyncio.gather(
            self.worldbuilder.update_world(request, context=context),
            self.charactermanager.update_characters(request, context=context),
            self.plotweaver.weave_plot(request, context=context)
        )
        
        if callback:
             await callback("Updating", "Knowledge Graph is being updated...")

        # Note: Agents already sync with graph in their update_ methods.
        # We just need to ensure the graph is persisted.

        self._save_state()
        
        return world_state, character_update, plot_point

    async def plan(self, user_input: str, callback: Optional[Callable] = None) -> MindState:
        """
        Runs only the subconscious planning phase.
        """
        request = StoryRequest(user_input=user_input)
        context = await self._get_context()

        if callback:
            await callback("KickLang Operation: Planning", "Invoking Subconscious Planner...")

        result = await self.planner.plan_pipeline(request, context=context, callback=callback)
        
        self._save_state()
        
        return result
