from typing import Optional
import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Automatically locate and load .env files from current working directory or subfolders
find_path = find_dotenv(usecwd=True)
if find_path:
    load_dotenv(find_path)

if os.path.exists("sherkat_os/.env"):
    load_dotenv("sherkat_os/.env")
if os.path.exists(".env"):
    load_dotenv(".env")
if os.path.exists("../.env"):
    load_dotenv("../.env")

class Settings(BaseSettings):
    """
    Enterprise settings management for SherkatOS.
    Loads environment variables from a .env file or environment.
    """
    model_config = SettingsConfigDict(
        env_file=(".env", "sherkat_os/.env", "../.env"),
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

    default_model: str = "gemini-3.5-flash-lite"
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
