import os
import asyncio
import json
from typing import Type, TypeVar, Protocol, runtime_checkable, Any
from pydantic import BaseModel
from google import genai
from mistralai import Mistral
import httpx
from rich.console import Console, Group
from rich.panel import Panel
from rich.syntax import Syntax
from src.shared.config import settings, LLMProvider

T = TypeVar("T", bound=BaseModel)
console = Console()

def _log_llm_event(provider: str, model: str, prompt: str, response: Any):
    """Log LLM communication using rich panels."""
    prompt_content = Syntax(prompt, "markdown", theme="monokai", word_wrap=True)
    
    if isinstance(response, BaseModel):
        res_text = response.model_dump_json(indent=2)
        res_lang = "json"
    elif isinstance(response, (dict, list)):
        res_text = json.dumps(response, indent=2)
        res_lang = "json"
    else:
        res_text = str(response)
        res_lang = "json" if res_text.strip().startswith(("{", "[")) else "markdown"

    response_content = Syntax(res_text, res_lang, theme="monokai", word_wrap=True)

    console.print(Group(
        Panel(prompt_content, title=f"[bold blue]LLM Prompt ({provider}: {model})[/bold blue]", border_style="blue"),
        Panel(response_content, title=f"[bold green]LLM Response ({provider}: {model})[/bold green]", border_style="green")
    ))

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
        res_text = response.text
        _log_llm_event("Gemini", self.model_name, prompt, res_text)
        return res_text

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': schema
            }
        )
        parsed = response.parsed if response.parsed else schema.model_validate_json(response.text)
        _log_llm_event("Gemini", self.model_name, prompt, parsed)
        return parsed

class MistralService:
    def __init__(self):
        api_key = settings.mistral_api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is not set")
        
        self.client = Mistral(api_key=api_key)
        self.model_name = settings.mistral_model

    async def generate_text(self, prompt: str) -> str:
        retries = 0
        max_retries = 3
        base_delay = 5.0

        while True:
            try:
                response = await self.client.chat.complete_async(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                res_text = response.choices[0].message.content
                _log_llm_event("Mistral", self.model_name, prompt, res_text)
                return res_text
            except Exception as e:
                if "429" in str(e):
                    if retries < max_retries:
                        delay = base_delay * (2 ** retries)
                        console.print(f"[bold yellow]Mistral 429 Rate Limit. Retrying in {delay}s... (Attempt {retries + 1}/{max_retries})[/bold yellow]")
                        await asyncio.sleep(delay)
                        retries += 1
                        continue
                    else:
                        console.print(f"[bold red]Mistral 429 Rate Limit exceeded max retries ({max_retries}).[/bold red]")
                        raise e
                else:
                    raise e

    async def generate_structured(self, prompt: str, schema: Type[T]) -> T:
        retries = 0
        max_retries = 3
        base_delay = 5.0

        while True:
            try:
                response = await self.client.chat.parse_async(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format=schema
                )
                parsed = response.choices[0].message.parsed
                _log_llm_event("Mistral", self.model_name, prompt, parsed)
                return parsed
            except Exception as e:
                # Check for rate limit error (usually 429 in string representation)
                if "429" in str(e):
                    if retries < max_retries:
                        delay = base_delay * (2 ** retries)
                        console.print(f"[bold yellow]Mistral 429 Rate Limit. Retrying in {delay}s... (Attempt {retries + 1}/{max_retries})[/bold yellow]")
                        await asyncio.sleep(delay)
                        retries += 1
                        continue
                    else:
                        console.print(f"[bold red]Mistral 429 Rate Limit exceeded max retries ({max_retries}).[/bold red]")
                        raise e
                else:
                    raise e

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
        res_text = response.json()["response"]
        _log_llm_event("Ollama", self.model_name, prompt, res_text)
        return res_text

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
        parsed = schema.model_validate_json(data)
        _log_llm_event("Ollama", self.model_name, prompt, parsed)
        return parsed

def get_llm_service() -> LLMService:
    if settings.llm_provider == LLMProvider.GEMINI:
        return GeminiService()
    elif settings.llm_provider == LLMProvider.MISTRAL:
        return MistralService()
    elif settings.llm_provider == LLMProvider.OLLAMA:
        return OllamaService()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
