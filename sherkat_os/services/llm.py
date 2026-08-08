from typing import Type, TypeVar, Any, Dict, Optional
import logging
from pydantic import BaseModel
from langchain_core.messages import AIMessage
from sherkat_os.config.settings import settings

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger("sherkat_os.services.llm")

class LLMService:
    """
    Enterprise LLM Factory service supporting live ChatModels (Gemini Flash Lite / OpenAI).
    Raises an explicit error when no API key is provided, preventing fallback guessing.
    """
    def __init__(self):
        self.default_model = settings.default_model
        self.temperature = settings.temperature

    def get_model(self) -> Any:
        """
        Returns a configured live LangChain ChatModel instance.
        Raises ValueError if no valid API key is present in environment or .env file.
        """
        google_key = settings.get_effective_google_api_key()
        if google_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                model_name = self.default_model if self.default_model else "gemini-3.5-flash-lite"
                logger.info(f"Initializing live ChatGoogleGenerativeAI with model: '{model_name}'")
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=google_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.error(f"Failed to initialize ChatGoogleGenerativeAI: {e}")
                raise RuntimeError(f"Error initializing ChatGoogleGenerativeAI ({self.default_model}): {e}")

        openai_key = settings.get_effective_openai_api_key()
        if openai_key:
            try:
                from langchain_openai import ChatOpenAI
                model_name = "gpt-4o" if "gpt" not in self.default_model else self.default_model
                logger.info(f"Initializing live ChatOpenAI with model: '{model_name}'")
                return ChatOpenAI(
                    model=model_name,
                    api_key=openai_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.error(f"Failed to initialize ChatOpenAI: {e}")
                raise RuntimeError(f"Error initializing ChatOpenAI ({self.default_model}): {e}")

        # If no API Key is available and fallback_to_mock is False, raise explicit exception
        raise ValueError(
            "CRITICAL: No API Key found! Please configure GOOGLE_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in your .env file or environment."
        )

llm_service = LLMService()
