from src.shared.models import MindState

class StorytellerPlannerMemory:
    """
    StorytellerPlannerMemory v1.0
    Retrieves subconscious chains and compiles narrative output.
    """
    @staticmethod
    def compile_synthesis(state: MindState) -> str:
        """
        Output type: implicit cognitive flow.
        Rules:
        - dictionary minimal
        - sentence shortest
        - order strict: focus <<roles>>
        - goal: fast user attention draw
        """
        # Dictionary minimal style:
        # focus: [last step of plan]
        # researcher: [cue count]
        # analyst: [pattern count]
        # storyteller: [dream summary snippet]
        # planner: [plan step count]
        
        last_step = state.plan.steps[-1] if state.plan and state.plan.steps else "initial"
        dream_snippet = state.dream.narrative[:50] + "..." if state.dream else "none"
        
        # Sentence shortest / dictionary minimal
        synthesis = (
            f"focus: {last_step}. "
            f"researcher: {len(state.cues)} cues. "
            f"analyst: {len(state.patterns)} patterns. "
            f"storyteller: {dream_snippet} "
            f"planner: {len(state.plan.steps) if state.plan else 0} steps."
        )
        
        return synthesis
