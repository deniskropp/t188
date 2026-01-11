from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import networkx as nx
import os

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput, MindState, JournalEntry, LoopStatus
from src.shared.config import settings
from src.shared.suggestions import SuggestionService
from src.shared.journal import SharedJournalService
from src.shared.quests import QuestOrchestrator

import asyncio
import json
from sse_starlette.sse import EventSourceResponse

# Status Manager for SSE tracking
class StatusManager:
    def __init__(self):
        self.queues: List[asyncio.Queue] = []

    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.queues.append(queue)
        return queue

    def unsubscribe(self, queue: asyncio.Queue):
        if queue in self.queues:
            self.queues.remove(queue)

    async def broadcast(self, op: str, message: str, data: Any = None):
        payload = json.dumps({"operation": op, "message": message, "data": data})
        for queue in self.queues:
            await queue.put(payload)

status_manager = StatusManager()

async def event_generator(request: Request):
    queue = await status_manager.subscribe()
    try:
        while True:
            if await request.is_disconnected():
                break
            data = await queue.get()
            yield data
    finally:
        status_manager.unsubscribe(queue)

app = FastAPI(
    title="MetaCognito API",
    description="API for the MetaCognito Storybook Orchestration Engine",
    version="0.1.0"
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def system_callback(op: str, message: str, data: Any = None):
    if "KickLang" in op or "Parsing" in op or "Synthesis" in op:
        quest_orchestrator.pulse_pipe(f"{op}: {message}")
    await status_manager.broadcast(op, message, data)

system = MetaCognito()
journal_service = SharedJournalService()
quest_orchestrator = QuestOrchestrator()

class ChatInput(BaseModel):
    message: str = Field(..., description="The user's input/request for the story")
    mind_state: Optional[MindState] = Field(None, description="Optional pre-generated subconscious plan")

class TransformInput(BaseModel):
    instruction: str = Field(..., description="The transformation instruction to apply to the graph")

class NodeData(BaseModel):
    id: str
    label: str
    type: str
    properties: Dict[str, Any]

class EdgeData(BaseModel):
    source: str
    target: str
    label: str

class GraphResponse(BaseModel):
    nodes: List[NodeData]
    edges: List[EdgeData]

@app.get("/api/events")
async def events(request: Request):
    """Real-time event stream for system status updates."""
    return EventSourceResponse(event_generator(request))

@app.get("/api/status")
async def get_status() -> Dict[str, Any]:
    """Get the current system status."""
    return {
        "status": "online",
        "node_count": len(system.graph_store.graph.nodes),
        "edge_count": len(system.graph_store.graph.edges),
        "provider": settings.llm_provider
    }

@app.get("/api/graph", response_model=GraphResponse)
async def get_graph() -> GraphResponse:
    """Returns the current graph state."""
    graph = system.graph_store.graph
    
    nodes = []
    for node_id, data in graph.nodes(data=True):
        nodes.append(NodeData(
            id=str(node_id),
            label=data.get("properties", {}).get("name") or data.get("name") or str(node_id),
            type=data.get("type", "Unknown"),
            properties=data.get("properties", {})
        ))
    
    seen_edges = set()
    edges = []
    for u, v, data in graph.edges(data=True):
        label = data.get("key") or data.get("type") or "related_to"
        edge_key = (u, v, label)
        if edge_key not in seen_edges:
            edges.append(EdgeData(
                source=str(u),
                target=str(v),
                label=label
            ))
            seen_edges.add(edge_key)
        
    return GraphResponse(nodes=nodes, edges=edges)
    
@app.get("/api/suggestions")
async def get_suggestions() -> Dict[str, List[str]]:
    """Generate and return story suggestions based on the current context."""
    try:
        graph_summary = system.graph_store.get_summary()
        suggestions = await SuggestionService.get_suggestions(context=graph_summary)
        return {"suggestions": suggestions}
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(input: ChatInput) -> Dict[str, Any]:
    """Process a story request and return the narrative segment."""
    print(f"Received chat request: {input.message}")
    try:
        # We pass the mind_state directly if the frontend has one staged
        result: SynthesisOutput = await system.process_story_request(input.message, callback=system_callback, mind_state=input.mind_state)
        print(f"Successfully processed: {result.narrative_segment[:50]}...")
        return {
            "reply": result.narrative_segment,
            "graph_nodes": len(system.graph_store.graph.nodes)
        }
    except Exception as e:
        print(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan")
async def plan(input: ChatInput) -> MindState:
    """Run only the subconscious planning phase."""
    print(f"Received plan request: {input.message}")
    try:
        mind_state = await system.plan(input.message, callback=system_callback)
        return mind_state
    except Exception as e:
        print(f"Error processing plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history() -> List[Dict[str, str]]:
    """Return the narrative history logs."""
    return system.history

@app.post("/api/reset")
async def reset_system() -> Dict[str, str]:
    """Unified reset of Graph and History."""
    try:
        system.reset()
        return {"status": "success", "message": "System state reset successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transform")
async def transform(input: TransformInput) -> Dict[str, Any]:
    """Apply a narrative transformation for Knowledge Graph updates."""
    print(f"Received transform request: {input.instruction}")
    try:
        await system.transform_state(input.instruction)
        print(f"Successfully transformed: {input.instruction}")
        return {
            "status": "success",
            "message": f"Transformation applied: {input.instruction}",
            "graph_nodes": len(system.graph_store.graph.nodes)
        }
    except Exception as e:
        print(f"Error processing transform: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clear")
async def clear_graph() -> Dict[str, Any]:
    """Clear the Knowledge Graph and delete persistent storage (Legacy compatibility)."""
    try:
        system.reset()
        return {
            "status": "success",
            "message": "Knowledge Graph and history cleared."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# "The Loop" Narrative Engine Endpoints

@app.get("/api/loop/status", response_model=LoopStatus)
async def get_loop_status() -> LoopStatus:
    """Get the current neurocognitive status and quest progress."""
    dopamine = journal_service.calculate_dopamine_density()
    flow = journal_service.calculate_flow_time()
    engagement = journal_service.calculate_engagement_index()
    return quest_orchestrator.get_loop_status(dopamine, flow, engagement)

@app.post("/api/loop/entry")
async def create_journal_entry(entry_data: Dict[str, Any]) -> JournalEntry:
    """Log a new artistic action or reflection to the shared journal."""
    try:
        entry = await journal_service.log_entry(
            action_type=entry_data.get("action_type", "stroke"),
            content=entry_data.get("content", ""),
            metadata=entry_data.get("metadata", {}),
            sentiment=entry_data.get("sentiment")
        )
        # Proactively update quest progress based on actions
        if entry.action_type == "stroke":
            # Example tracking: update quest q1 if nodes are being added
            # For now, just increment a counter in quest orchestrator
            # In a real scenario, this would be tied to GraphStore events
            pass
            
        return entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/loop/quest/claim/{quest_id}")
async def claim_quest_badge(quest_id: str):
    """Claim the badge for a completed quest."""
    badge = quest_orchestrator.claim_badge(quest_id)
    if not badge:
        raise HTTPException(status_code=400, detail="Quest not completed or badge already claimed.")
    return badge
