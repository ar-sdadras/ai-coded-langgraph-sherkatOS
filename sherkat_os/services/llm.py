from typing import Type, TypeVar, Any, Dict, Optional, Union, List, get_origin, get_args
import json
import logging
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, AIMessage
from sherkat_os.config.settings import settings

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger("sherkat_os.services.llm")

def mock_generate_value(field_type: Any, field_name: str, prompt_text: str = "") -> Any:
    """
    Recursively builds valid sample values for Pydantic fields.
    """
    origin = get_origin(field_type)
    args = get_args(field_type)
    
    # Unwrap Optional[T] / Union[T, None]
    if origin is Union:
        non_none = [a for a in args if a is not type(None)]
        if non_none:
            field_type = non_none[0]
            origin = get_origin(field_type)
            args = get_args(field_type)

    # Direct Pydantic BaseModel instance
    if isinstance(field_type, type) and issubclass(field_type, BaseModel):
        sub_fields = {}
        for fname, finfo in field_type.model_fields.items():
            sub_fields[fname] = mock_generate_value(finfo.annotation, fname, prompt_text)
        return field_type(**sub_fields)

    # List of items
    if origin is list or origin is List or "list" in str(field_type).lower():
        item_type = args[0] if args else str
        if isinstance(item_type, type) and issubclass(item_type, BaseModel):
            item_obj = mock_generate_value(item_type, field_name, prompt_text)
            return [item_obj]
        else:
            if "endpoint" in field_name:
                return ["GET /api/v1/status", "POST /api/v1/simulate"]
            return ["Enterprise Strategy", "Autonomous Agent Subgraphs"]

    # Dict type
    if origin is dict or origin is Dict or "dict" in str(field_type).lower():
        return {"status": "validated", "tier": "enterprise"}

    # String type check FIRST before keyword checks
    if field_type == str or "str" in str(field_type).lower():
        return f"Simulated {field_name.replace('_', ' ').title()}"
        
    # Numeric and Boolean types
    if field_type == bool or "bool" in str(field_type).lower():
        return True
    elif field_type == float or "float" in str(field_type).lower():
        return 95.5
    elif field_type == int or "int" in str(field_type).lower():
        return 10
    else:
        return f"Generated {field_name}"

class SchemaAwareMockRunnable:
    """
    Simulates a LangChain runnable with structured output bound to a Pydantic schema.
    Dynamically generates valid Pydantic model instances matching the schema definition.
    """
    def __init__(self, schema: Type[T]):
        self.schema = schema

    def invoke(self, input_data: Any, config: Optional[Dict[str, Any]] = None) -> T:
        prompt_text = str(input_data)
        
        field_values = {}
        for field_name, field_info in self.schema.model_fields.items():
            if field_info.default is not None and str(field_info.default) != "PydanticUndefined":
                field_values[field_name] = field_info.default
            else:
                field_values[field_name] = mock_generate_value(field_info.annotation, field_name, prompt_text)

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
