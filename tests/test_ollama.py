import asyncio
import unittest
from unittest.mock import AsyncMock, patch
from pydantic import BaseModel
from src.shared.llm import OllamaService
from src.shared.config import settings

class TestSchema(BaseModel):
    name: str
    age: int

class TestOllamaService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure we use OLLAMA for testing
        settings.ollama_base_url = "http://localhost:11434"
        settings.ollama_model = "llama3"
        self.service = OllamaService()

    @patch("httpx.AsyncClient.post")
    async def test_generate_text(self, mock_post):
        # Mock response
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Hello world"}
        mock_post.return_value = mock_response

        result = await self.service.generate_text("Say hello")
        
        self.assertEqual(result, "Hello world")
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "/api/generate")
        self.assertEqual(kwargs["json"]["prompt"], "Say hello")

    @patch("httpx.AsyncClient.post")
    async def test_generate_structured(self, mock_post):
        # Mock response
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": '{"name": "John", "age": 30}'}
        mock_post.return_value = mock_response

        result = await self.service.generate_structured("Tell me about John", TestSchema)
        
        self.assertIsInstance(result, TestSchema)
        self.assertEqual(result.name, "John")
        self.assertEqual(result.age, 30)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["format"], "json")

if __name__ == "__main__":
    unittest.main()
