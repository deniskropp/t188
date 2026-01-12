import pytest
from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput

@pytest.mark.asyncio
async def test_process_story_request_flow(mock_llm_service):
    system = MetaCognito()
    user_input = "Hero enters the dragon cave"
    
    result = await system.process_story_request(user_input)
    
    assert isinstance(result, SynthesisOutput)
    assert result.narrative_segment is not None
    assert "Mocked narrative segment" in result.narrative_segment
