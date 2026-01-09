from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MetaCognito"
    max_refinement_steps: int = 3
    critic_threshold: float = 0.7
    
    # Prompt Templates (Basic examples)
    storyteller_prompt: str = "You are a master storyteller..."

    model_config = SettingsConfigDict(env_prefix="METASYS_")

settings = Settings()
