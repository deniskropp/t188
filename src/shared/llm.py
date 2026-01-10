import os
from typing import Type, TypeVar, Protocol, runtime_checkable
from pydantic import BaseModel
from google import genai
from mistralai import Mistral
import httpx
from src.shared.config import settings, LLMProvider

T = TypeVar("T", bound=BaseModel)

@runtime_checkable
class LLMService(Protocol):
    async def generate_text(self, prompt: str) -> str:
        ...

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        ...

class GeminiService:
    def __init__(self):
        api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = settings.gemini_model

    async def generate_text(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': schema
            }
        )
        if response.parsed:
             return response.parsed
        return schema.model_validate_json(response.text)

class MistralService:
    def __init__(self):
        api_key = settings.mistral_api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is not set")
        
        self.client = Mistral(api_key=api_key)
        self.model_name = settings.mistral_model

    async def generate_text(self, prompt: str) -> str:
        response = await self.client.chat.complete_async(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        response = await self.client.chat.parse_async(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format=schema
        )
        return response.choices[0].message.parsed

class OllamaService:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model_name = settings.ollama_model
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=600.0)

    async def generate_text(self, prompt: str) -> str:
        response = await self.client.post(
            "/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        prompt_with_schema = f"{prompt}\n\nReturn JSON only, matching this schema: {schema.model_json_schema()}"
        response = await self.client.post(
            "/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt_with_schema,
                "format": "json",
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()["response"]
        return schema.model_validate_json(data)

def get_llm_service() -> LLMService:
    if settings.llm_provider == LLMProvider.GEMINI:
        return GeminiService()
    elif settings.llm_provider == LLMProvider.MISTRAL:
        return MistralService()
    elif settings.llm_provider == LLMProvider.OLLAMA:
        return OllamaService()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
