import pytest
from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput

@pytest.mark.asyncio
async def test_process_story_request_flow():
    system = MetaCognito()
    user_input = "Hero enters the dragon cave"
    
    result = await system.process_story_request(user_input)
    
    assert isinstance(result, SynthesisOutput)
    # Since we are using mock services currently, we expect some string result
    assert result.narrative_segment is not None
    assert len(result.narrative_segment) > 0
