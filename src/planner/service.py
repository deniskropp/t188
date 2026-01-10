from typing import List
from pydantic import BaseModel
from src.shared.base import BaseRole
from src.shared.models import (
    StoryRequest, 
    SubconsciousCue, 
    LatentPattern, 
    DreamNarrative, 
    ImplicitPlan,
    MindState
)

class CueList(BaseModel): 
    cues: List[SubconsciousCue]

class PatternList(BaseModel):
    patterns: List[LatentPattern]

class ResearcherRole(BaseRole):
    async def find_cues(self, request: StoryRequest, context: str = "") -> List[SubconsciousCue]:
        prompt = f"""
        Role: Researcher (Subconscious)
        Objective: FIND subconscious data auto.
        
        Analyze the request and context to identify hidden cues, themes, or missing data points.
        
        Context: {context}
        Request: "{request.user_input}"
        
        Output a list of SubconsciousCue objects.
        """
        # Note: We use a list wrapper here because generate_structured expects a BaseModel
        result = await self._generate_structured(prompt, CueList)
        return result.cues

class AnalystRole(BaseRole):
    async def cluster_patterns(self, cues: List[SubconsciousCue], context: str = "") -> List[LatentPattern]:
        cues_str = "\n".join([f"- {c.cue} ({c.context})" for c in cues])
        prompt = f"""
        Role: Analyst (Subconscious)
        Objective: CLUSTER patterns latent.
        
        Analyze the subconscious cues and group them into latent patterns.
        
        Cues:
        {cues_str}
        
        Context: {context}
        
        Output a list of LatentPattern objects.
        """
        result = await self._generate_structured(prompt, PatternList)
        return result.patterns

class SubconsciousStorytellerRole(BaseRole):
    async def summarize_dream(self, patterns: List[LatentPattern], context: str = "") -> DreamNarrative:
        patterns_str = "\n".join([f"- {p.pattern} (strength: {p.strength})" for p in patterns])
        prompt = f"""
        Role: Storyteller (Subconscious)
        Objective: SUMMARIZE dream narratives internal.
        
        Weave the latent patterns into a concise internal "dream narrative" that captures the essence of the subconscious state.
        
        Patterns:
        {patterns_str}
        
        Context: {context}
        
        Output a DreamNarrative object.
        """
        return await self._generate_structured(prompt, DreamNarrative)

class SubconsciousPlannerRole(BaseRole):
    async def sequence_plan(self, dream: DreamNarrative, request: StoryRequest, context: str = "") -> ImplicitPlan:
        prompt = f"""
        Role: Planner (Subconscious)
        Objective: SEQUENCE intuitive paths hidden.
        
        Based on the internal dream narrative and the user request, sequence a series of intuitive, hidden steps for the main orchestration.
        
        Dream: {dream.narrative}
        Request: "{request.user_input}"
        Context: {context}
        
        Output an ImplicitPlan object.
        """
        return await self._generate_structured(prompt, ImplicitPlan)
