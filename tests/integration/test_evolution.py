import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys

# Mock google.generativeai as it might not be installed in the test env
mock_genai_lib = MagicMock()
sys.modules["google.generativeai"] = mock_genai_lib

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput, WorldState, CharacterUpdate, PlotPoint
from src.shared.config import settings
import src.shared.llm # Ensure module is loaded

@pytest.mark.asyncio
async def test_refinement_loop():
    from unittest.mock import AsyncMock, patch
    # Mock the LLM service to return valid data so the loop can proceed
    with patch("src.shared.llm.GoogleGenAIService") as MockServiceClass:
        mock_llm = AsyncMock()
        MockServiceClass.return_value = mock_llm
        
        # Setup returns
        from src.shared.models import WorldState, CharacterUpdate, PlotPoint, Feedback
        mock_llm.generate_structured.side_effect = [
            WorldState(locations=["L"], concepts=["C"]), 
            CharacterUpdate(characters=["C"], traits=[], interactions=[]),
            PlotPoint(events=["E"], precedence=[]),
            Feedback(score=1.0, critique="Good", suggestion="", approved=True)
        ]
        mock_llm.generate_text.return_value = "Long enough story content for the test"

        system = MetaCognito()
        
        # Run a normal request
        res = await system.process_story_request("A short test")
        
        # Should be approved because default mock output is long enough.
        assert "[Warning: Critic usage limit reached" not in res.narrative_segment

@pytest.mark.asyncio
async def test_refinement_loop_rejection():
    from unittest.mock import AsyncMock, patch
    # Patch here as well to avoid init error
    with patch("src.shared.llm.GoogleGenAIService") as MockServiceClass:
        mock_llm = AsyncMock()
        MockServiceClass.return_value = mock_llm
        
        # We only need the structured calls for world/char/plot to succeed first
        from src.shared.models import WorldState, CharacterUpdate, PlotPoint
        mock_llm.generate_structured.side_effect = [
            WorldState(locations=["L"], concepts=["C"]), 
            CharacterUpdate(characters=["C"], traits=[], interactions=[]),
            PlotPoint(events=["E"], precedence=[])
        ]
        # Storyteller
        mock_llm.generate_text.return_value = "Story"

        # Force rejection by mocking the critic on the instance
        system = MetaCognito()
        
        # Mock critique method
        from src.shared.models import Feedback
        
        call_count = 0
        
        async def mock_critique(narrative, world):
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
