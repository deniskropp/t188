from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import networkx as nx
import os

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput
from src.shared.config import settings
from src.shared.suggestions import SuggestionService

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

system = MetaCognito()

class ChatInput(BaseModel):
    message: str = Field(..., description="The user's input/request for the story")

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
        result: SynthesisOutput = await system.process_story_request(input.message)
        print(f"Successfully processed: {result.narrative_segment[:50]}...")
        return {
            "reply": result.narrative_segment,
            "graph_nodes": len(system.graph_store.graph.nodes)
        }
    except Exception as e:
        print(f"Error processing chat: {e}")
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
    """Clear the Knowledge Graph and delete persistent storage."""
    try:
        system.graph_store.clear()
        if os.path.exists(settings.graph_storage_path):
            os.remove(settings.graph_storage_path)
            
        return {
            "status": "success",
            "message": "Knowledge Graph cleared and persistent storage deleted."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
