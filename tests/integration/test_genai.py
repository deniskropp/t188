import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import sys

# Mock google.generativeai as it might not be installed in the test env
mock_genai_lib = MagicMock()
sys.modules["google.generativeai"] = mock_genai_lib

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput, WorldState, CharacterUpdate, PlotPoint, Feedback
import src.shared.llm # Ensure module is loaded for patch to work

@pytest.mark.asyncio
async def test_metacognito_with_mock_genai():
    # Patch the GoogleGenAIService at the source where it's used or imported
    # Since we import it inside the methods, we need to patch 'src.shared.llm.GoogleGenAIService'
    # But wait, we import it inside the methods in the services. 
    # e.g. "from src.shared.llm import GoogleGenAIService" inside update_world
    
    with patch("src.shared.llm.genai") as mock_genai_mod:
        # Mock configuration to avoid API Key error
        mock_genai_mod.configure = AsyncMock()
        
        # We also need to mock the Service class instantiation itself if we want to intercept calls easily.
        # Or we can let it instantiate but mock the internal model.
        
        # Let's patch the class to return a mock instance
        with patch("src.shared.llm.GoogleGenAIService") as MockServiceClass:
            # Setup the mock instance
            mock_llm = AsyncMock()
            MockServiceClass.return_value = mock_llm
            
            # Setup return values for the mock methods
            mock_llm.generate_structured.side_effect = [
                WorldState(locations=["MockLoc"], concepts=["MockConcept"]), # WorldBuilder
                CharacterUpdate(characters=["MockChar"], traits=[], interactions=[]), # CharManager
                PlotPoint(events=["MockEvent"], precedence=[]), # PlotWeaver
                Feedback(score=1.0, critique="Great", suggestion="", approved=True) # Critic
            ]
            
            mock_llm.generate_text.return_value = "Generated Story Content" # Storyteller
            
            # Additional calls for critic in loop?
            # The side_effect list needs to be long enough if loops happen.
            # But here we simulate immediate approval.
            
            system = MetaCognito()
            result = await system.process_story_request("Test Input")
            
            assert "Generated Story Content" in result.narrative_segment
            assert mock_llm.generate_structured.call_count >= 4
            assert mock_llm.generate_text.call_count >= 1
