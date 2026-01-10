import asyncio
import time
import random
from typing import Optional, Callable
from src.shared.graph import GraphStore
from src.shared.models import StoryRequest, MindState, GraphNode, GraphEdge, KeyValue
from src.planner.service import (
    ResearcherRole, 
    AnalystRole, 
    SubconsciousStorytellerRole, 
    SubconsciousPlannerRole
)

class MetaCognitoPlanner:
    """
    MetaCognito/Planner v1.1
    Purpose: manage subconscious planning via hidden role chains.
    """
    def __init__(self, graph_store: GraphStore):
        self.graph_store = graph_store
        self.researcher = ResearcherRole(graph_store)
        self.analyst = AnalystRole(graph_store)
        self.storyteller = SubconsciousStorytellerRole(graph_store)
        self.planner = SubconsciousPlannerRole(graph_store)

    async def plan_pipeline(self, request: StoryRequest, context: str = "", callback: Optional[Callable] = None) -> MindState:
        """
        Role operations flow: Researcher → Analyst → Storyteller → Planner.
        """
        if callback:
            await callback("Subconscious", "Researcher is finding cues...")
        
        # 1. FIND subconscious cues
        cues = await self.researcher.find_cues(request, context=context)
        
        if callback:
            await callback("Subconscious", "Analyst is clustering patterns...")
        
        patterns = await self.analyst.cluster_patterns(cues, context=context)
        
        if callback:
            await callback("Subconscious", "Storyteller is summarizing dream...")
            
        dream = await self.storyteller.summarize_dream(patterns, context=context)
        
        if callback:
            await callback("Subconscious", "Planner is sequencing intuitive paths...")
            
        plan = await self.planner.sequence_plan(dream, request, context=context)
        
        # PERSISTENCE: Convert MindState components to Graph elements
        nodes = []
        edges = []
        
        timestamp = int(time.time())
        rand_id = random.randint(1000, 9999)
        session_id = f"sub_session_{timestamp}_{rand_id}"
        
        nodes.append(GraphNode(
            id=session_id,
            type="SubconsciousSession",
            properties=[
                KeyValue(key="name", value=f"Session at {timestamp}"),
                KeyValue(key="request", value=request.user_input)
            ]
        ))
        
        for i, cue in enumerate(cues):
            cue_id = f"cue_{timestamp}_{i}"
            nodes.append(GraphNode(
                id=cue_id,
                type="SubconsciousCue",
                properties=[
                    KeyValue(key="description", value=cue.cue),
                    KeyValue(key="context", value=cue.context)
                ]
            ))
            edges.append(GraphEdge(source=session_id, target=cue_id, relationship="identifies_cue"))
            
        for i, p in enumerate(patterns):
            p_id = f"pattern_{timestamp}_{i}"
            nodes.append(GraphNode(
                id=p_id,
                type="LatentPattern",
                properties=[
                    KeyValue(key="description", value=p.pattern),
                    KeyValue(key="strength", value=str(p.strength))
                ]
            ))
            edges.append(GraphEdge(source=session_id, target=p_id, relationship="discovers_pattern"))
            
        if dream:
            dream_id = f"dream_{timestamp}"
            nodes.append(GraphNode(
                id=dream_id,
                type="DreamNarrative",
                properties=[KeyValue(key="description", value=dream.narrative)]
            ))
            edges.append(GraphEdge(source=session_id, target=dream_id, relationship="forms_dream"))
            
        if plan:
            plan_id = f"plan_{timestamp}"
            nodes.append(GraphNode(
                id=plan_id,
                type="ImplicitPlan",
                properties=[KeyValue(key="description", value="; ".join(plan.steps))]
            ))
            edges.append(GraphEdge(source=session_id, target=plan_id, relationship="sequences_plan"))

        # Sync with Graph Store
        for node in nodes:
            self.graph_store.add_node(node)
        for edge in edges:
            self.graph_store.add_edge(edge)
            
        return MindState(
            cues=cues,
            patterns=patterns,
            dream=dream,
            plan=plan,
            nodes=nodes,
            edges=edges
        )
