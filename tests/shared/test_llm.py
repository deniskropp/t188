import pytest
from unittest.mock import MagicMock, patch
from src.shared.llm import OllamaService
from src.shared.config import settings
from pydantic import BaseModel

class SchemaForTest(BaseModel):
    name: str
    age: int

@pytest.mark.asyncio
class TestOllamaService:
    @pytest.fixture(autouse=True)
    def setup(self):
        settings.ollama_base_url = "http://localhost:11434"
        settings.ollama_model = "llama3"
        self.service = OllamaService()

    @patch("httpx.AsyncClient.post")
    async def test_generate_text(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Hello world"}
        mock_post.return_value = mock_response

        result = await self.service.generate_text("Say hello")
        
        assert result == "Hello world"
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "/api/generate"
        assert kwargs["json"]["prompt"] == "Say hello"

    @patch("httpx.AsyncClient.post")
    async def test_generate_structured(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": '{"name": "John", "age": 30}'}
        mock_post.return_value = mock_response

        result = await self.service.generate_structured("Tell me about John", SchemaForTest)
        
        assert isinstance(result, SchemaForTest)
        assert result.name == "John"
        assert result.age == 30
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["format"] == "json"
