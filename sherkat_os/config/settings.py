from typing import Optional
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Enterprise settings management for SherkatOS.
    Loads environment variables from a .env file or environment.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # LLM Settings
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    def get_effective_google_api_key(self) -> Optional[str]:
        return self.google_api_key or self.gemini_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    def get_effective_openai_api_key(self) -> Optional[str]:
        return self.openai_api_key or os.getenv("OPENAI_API_KEY")

    default_model: str = "gemini-2.0-flash-lite"
    temperature: float = 0.2
    fallback_to_mock: bool = False # Require live LLM API key; do not guess
    
    # Storage & Export Settings
    output_dir: str = "output"
    
    # Graph Guardrail Settings
    max_retries: int = 3
    
    # Logging Settings
    log_level: str = "INFO"

# Global settings instance
settings = Settings()
