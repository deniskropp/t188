import pytest
from unittest.mock import MagicMock, patch
from src.shared.suggestions import SuggestionService
from src.shared.models import SuggestionList

@pytest.mark.asyncio
async def test_get_suggestions_success():
    mock_llm = MagicMock()
    # mock generate_structured to be an async method
    async def mock_generate(*args, **kwargs):
        return SuggestionList(suggestions=["Sugg 1", "Sugg 2"])
    
    mock_llm.generate_structured = mock_generate
    
    with patch("src.shared.suggestions.get_llm_service", return_value=mock_llm):
        suggestions = await SuggestionService.get_suggestions("context")
        assert len(suggestions) == 2
        assert suggestions[0] == "Sugg 1"

@pytest.mark.asyncio
async def test_get_suggestions_fallback():
    mock_llm = MagicMock()
    async def mock_generate_fail(*args, **kwargs):
        raise Exception("LLM Error")
    
    mock_llm.generate_structured = mock_generate_fail
    
    with patch("src.shared.suggestions.get_llm_service", return_value=mock_llm):
        # Should return fallback static list
        suggestions = await SuggestionService.get_suggestions("context")
        assert len(suggestions) > 0
        from src.shared.suggestions import STORY_SUGGESTIONS
        assert suggestions == STORY_SUGGESTIONS
