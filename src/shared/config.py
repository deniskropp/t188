from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMProvider(str, Enum):
    GEMINI = "gemini"
    MISTRAL = "mistral"
    OLLAMA = "ollama"


class Settings(BaseSettings):
    app_name: str = "MetaCognito"
    max_refinement_steps: int = 3
    critic_threshold: float = 0.7
    
    google_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash-exp"
    
    mistral_api_key: str | None = None
    mistral_model: str = "mistral-medium-latest"
    
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "hf.co/tensorblock/NSFW_DPO_Noromaid-7b-GGUF"
    
    llm_provider: LLMProvider = LLMProvider.MISTRAL
    
    graph_storage_path: str = "knowledge_graph.json"
    
    # Prompt Templates (Basic examples)
    storyteller_prompt: str = "You are a master storyteller..."

    model_config = SettingsConfigDict(env_prefix="METASYS_")

settings = Settings()
