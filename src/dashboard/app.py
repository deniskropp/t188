from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import networkx as nx

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput

app = FastAPI(title="MetaCognito Dashboard")
system = MetaCognito()

templates = Jinja2Templates(directory="src/dashboard/templates")

class ChatInput(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/graph")
async def get_graph():
    """Returns the current graph state as Cytoscape elements."""
    # Convert networkx graph to cytoscape format manual or via utility
    # We want a simple usage for frontend: nodes and edges
    data = nx.node_link_data(system.graph_store.graph)
    
    # Transform for cytoscape.js
    elements = []
    # networkx node_link_data might return 'nodes' and 'links' (default)
    # but verify what data contains
    
    for node in data["nodes"]:
        elements.append({
            "data": {
                "id": str(node["id"]), # Ensure string
                "label": node.get("properties", {}).get("name", str(node["id"])),
                "color": "#ff0000" if "Event" in node.get("type", "") else "#00ff00" if "Character" in node.get("type", "") else "#0000ff"
            }
        })
    
    # In newer networkx, it might use 'links' or 'edges' depending on attrs=
    # Default is 'links'
    
    links_key = "links" if "links" in data else "edges"
    
    for link in data.get(links_key, []):
        elements.append({
            "data": {
                "source": str(link["source"]), 
                "target": str(link["target"]), 
                "label": link.get("key", "")
            }
        })
        
    return {"elements": elements}

@app.post("/api/chat")
async def chat(input: ChatInput):
    result = await system.process_story_request(input.message)
    return {"reply": result.narrative_segment}
