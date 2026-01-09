import os
from google import genai
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from src.shared.config import settings

T = TypeVar("T", bound=BaseModel)

class GoogleGenAIService:
    def __init__(self):
        if not settings.google_api_key:
            settings.google_api_key = os.getenv("GOOGLE_API_KEY") 
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is not set in configuration")
        
        self.client = genai.Client(api_key=settings.google_api_key)
        self.model_name = settings.gemini_model

    async def generate_text(self, prompt: str) -> str:
        """
        Generates free-form text based on the prompt.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        """
        Generates a structured object based on the prompt and Pydantic schema.
        Uses native structured output support.
        """
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': schema
            }
        )
        # response.parsed is available when response_schema is provided with Pydantic model
        # However, verifying if automatic parsing works as expected or if we need response.text parsing.
        # The new SDK documentation says response.parsed contains the parsed object if schema is provided.
        if response.parsed:
             return response.parsed
        
        # Fallback if parsed is None for some reason, though it shouldn't be with proper schema
        return schema.model_validate_json(response.text)
