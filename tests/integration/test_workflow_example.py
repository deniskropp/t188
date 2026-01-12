import pytest
import os
from src.metacognito.core import MetaCognito
from src.shared.models import (
    SynthesisOutput
)
from src.shared.config import settings

@pytest.mark.asyncio
async def test_workflow_example():
    """
    Automated test for the Workflow Example described in docs/Theatrical_Director_Model.md
    
    Workflow:
    1. Plan: /plan The hero enters a dark cave.
    2. Inspect: /state (Simulating inspection by asserting on the returned MindState)
    3. Execute: Look around. (Simulating performance)
    4. Adjust: /transform Add a hidden treasure chest to the cave.
    """
    
    # Determine the active provider and check for keys
    provider = settings.llm_provider
    api_key = None
    
    if provider == "gemini":
        api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            pytest.skip("GOOGLE_API_KEY not set for Gemini provider. Skipping.")
    elif provider == "mistral":
        api_key = settings.mistral_api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            pytest.skip("MISTRAL_API_KEY not set for Mistral provider. Skipping.")
    elif provider == "ollama":
        # Ollama usually doesn't need a key, but check connectivity could be good. 
        # For now assume it's fine or fail.
        pass
        
    print(f"Running workflow test with provider: {provider}")
    system = MetaCognito()
    system.reset() # Ensure clean state
    
    # --- Step 1: Plan ---
    print("\n--- Step 1: /plan ---")
    input_plan = "The hero enters a dark cave"
    mind_state = await system.plan(input_plan)
    
    # --- Step 2: Inspect ---
    print("--- Step 2: /state (Inspect) ---")
    assert mind_state is not None
    assert mind_state.plan is not None
    # Relaxed assertions for real LLM
    assert len(mind_state.cues) > 0, "Should generate specific subconscious cues"
    assert len(mind_state.plan.steps) > 0, "Should generate implicit plan steps"
    
    # Check for relevant keywords loosely
    plan_text = str(mind_state.plan).lower()
    cues_text = str(mind_state.cues).lower()
    assert "cave" in plan_text or "node" in plan_text or "enter" in plan_text or "hero" in plan_text
    print(f"Plan Steps: {mind_state.plan.steps}")
    
    # --- Step 3: Execute ---
    print("--- Step 3: Performance (Look around) ---")
    input_action = "Look around"
    # Pass the mind_state explicitly as if the frontend/CLI did it
    result = await system.process_story_request(input_action, mind_state=mind_state)
    
    assert isinstance(result, SynthesisOutput)
    print(f"Narrative: {result.narrative_segment}")
    assert len(result.narrative_segment) > 10, "Should generate a narrative description"
    
    # --- Step 4: Adjust ---
    print("--- Step 4: /transform ---")
    input_transform = "Add a hidden treasure chest to the cave"
    await system.transform_state(input_transform)
    
    # Verify the graph update
    found_chest = False
    print("Graph Nodes:")
    for node_id, data in system.graph_store.graph.nodes(data=True):
        print(f"- {node_id}: {data}")
        # Properties are stored flat in data dictionary in the actual graph store
        name = data.get("name", "").lower() + " " + data.get("type", "").lower() + " " + node_id.lower()
        if "chest" in name or "treasure" in name:
            found_chest = True
    
    assert found_chest, "The Treasure Chest node should exist in the graph after transformation."
    print("\nSuccess! Workflow completed as expected.")
