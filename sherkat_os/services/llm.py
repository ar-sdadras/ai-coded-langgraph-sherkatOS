from typing import Type, TypeVar, Any, Dict, Optional, Union
import json
import logging
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, AIMessage
from sherkat_os.config.settings import settings

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger("sherkat_os.services.llm")

class SchemaAwareMockRunnable:
    """
    Simulates a LangChain runnable with structured output bound to a Pydantic schema.
    Dynamically generates valid Pydantic model instances matching the schema definition.
    """
    def __init__(self, schema: Type[T]):
        self.schema = schema

    def invoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> T:
        # Extract prompt or message string for context
        prompt_text = ""
        if isinstance(input_data, list):
            prompt_text = " ".join([m.content if hasattr(m, 'content') else str(m) for m in input_data])
        elif hasattr(input_data, 'content'):
            prompt_text = str(input_data.content)
        else:
            prompt_text = str(input_data)

        # Generate sample data matching schema fields dynamically
        field_values = {}
        for field_name, field_info in self.schema.model_fields.items():
            field_type = field_info.annotation
            
            # Check default or generate standard defaults based on field name and type
            if field_info.default is not None and str(field_info.default) != "PydanticUndefined":
                field_values[field_name] = field_info.default
            elif "score" in field_name or "rating" in field_name or "count" in field_name:
                field_values[field_name] = 9
            elif "is_approved" in field_name or "approved" in field_name or "passed" in field_name:
                field_values[field_name] = True
            elif "percentage" in field_name or "rate" in field_name or "willingness" in field_name:
                field_values[field_name] = 85.0 if "float" in str(field_type).lower() else 85
            elif "list" in str(field_type).lower() or "List" in str(field_type):
                field_values[field_name] = ["Enterprise Strategy", "Autonomous Agent Nodes", "Scalable Infrastructure"]
            elif "dict" in str(field_type).lower() or "Dict" in str(field_type):
                field_values[field_name] = {"status": "validated", "tier": "enterprise"}
            elif field_type == str or "str" in str(field_type).lower():
                field_values[field_name] = f"Generated {field_name.replace('_', ' ').title()} for corporate simulation."
            elif field_type == bool:
                field_values[field_name] = True
            elif field_type == int:
                field_values[field_name] = 10
            elif field_type == float:
                field_values[field_name] = 95.5
            else:
                field_values[field_name] = None

        return self.schema(**field_values)

    async def ainvoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> T:
        return self.invoke(input_data, config)

class MockChatModel:
    """
    Fallback ChatModel implementation when live API keys are not provided.
    """
    def with_structured_output(self, schema: Type[T], **kwargs) -> SchemaAwareMockRunnable:
        return SchemaAwareMockRunnable(schema)

    def invoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> AIMessage:
        return AIMessage(content="SherkatOS autonomous agent simulation message processed.")

    async def ainvoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> AIMessage:
        return self.invoke(input_data, config)

class LLMService:
    """
    Enterprise LLM Factory service supporting live ChatModels and offline mock fallbacks.
    """
    def __init__(self):
        self.default_model = settings.default_model
        self.temperature = settings.temperature

    def get_model(self) -> Any:
        """
        Returns a configured LangChain ChatModel instance or a schema-aware fallback model.
        """
        if settings.google_api_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model=self.default_model if "gemini" in self.default_model else "gemini-1.5-pro",
                    google_api_key=settings.google_api_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.warning(f"Could not initialize ChatGoogleGenerativeAI: {e}. Falling back to MockChatModel.")
        
        if settings.openai_api_key:
            try:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model="gpt-4o" if "gpt" not in self.default_model else self.default_model,
                    api_key=settings.openai_api_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.warning(f"Could not initialize ChatOpenAI: {e}. Falling back to MockChatModel.")

        # Default fallback for testing and sandbox execution
        return MockChatModel()

llm_service = LLMService()
