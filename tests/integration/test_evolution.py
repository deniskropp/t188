import pytest
from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput, WorldState, CharacterUpdate, PlotPoint
from src.shared.config import settings

@pytest.mark.asyncio
async def test_refinement_loop():
    # To test the loop, we need the Critic to REJECT initially.
    # Our mock critic rejects if length < 5 words.
    
    # But our mock Storyteller produces a fixed string based on inputs.
    # "The story begins in the Forest of .... suddenyl ... " -> usually > 5 words.
    
    # We need to force a short output from Storyteller mock?
    # Or subclass MetaCognito to inject a strict critic?
    
    # Let's adjust the system config slightly for this test using mock? 
    # Or just rely on the logic that runs.
    
    system = MetaCognito()
    
    # Run a normal request
    res = await system.process_story_request("A short test")
    
    # Should be approved because default mock output is long enough.
    assert "[Warning: Critic usage limit reached" not in res.narrative_segment

@pytest.mark.asyncio
async def test_refinement_loop_rejection():
    # Force rejection by mocking the critic on the instance
    system = MetaCognito()
    
    # Mock critique method
    from src.shared.models import Feedback
    
    call_count = 0
    
    def mock_critique(narrative, world):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return Feedback(score=0.1, critique="Bad", suggestion="Retry", approved=False)
        return Feedback(score=1.0, critique="Good", suggestion="", approved=True)
        
    system.critic.critique = mock_critique
    
    res = await system.process_story_request("Retry test")
    
    # Should have run at least twice
    assert call_count == 2
    assert "[Warning: Critic usage limit reached" not in res.narrative_segment
