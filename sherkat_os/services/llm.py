from typing import Type, TypeVar, Any, Dict, Optional, Union, List, get_origin, get_args
import json
import logging
import os
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, AIMessage
from sherkat_os.config.settings import settings

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger("sherkat_os.services.llm")

# Professional contextual lookup dictionary for realistic offline fallback data
DOMAIN_FIELD_DEFAULTS = {
    "market_size_description": "Total Addressable Market (TAM) estimated at $14.8B for Autonomous Corporate AI Orchestration. Serviceable Addressable Market (SAM) is $3.2B targeting mid-to-large SaaS enterprises.",
    "suggested_value_proposition": "Fully autonomous multi-agent corporate simulation reducing department cross-functional friction by 80% with verified state persistence.",
    "product_vision": "Provide an enterprise-grade corporate sandbox where autonomous AI department heads collaborate seamlessly via LangGraph subgraphs.",
    "mvp_release_timeline": "12-week accelerated phase: Weeks 1-4 Subgraphs core, Weeks 5-8 API integrations, Weeks 9-12 Security and Load Audit.",
    "database_schema_concept": "Relational PostgreSQL database with org_sessions, department_states, agent_messages, and audit_logs tables with foreign key indexing.",
    "infrastructure_and_deployment": "Containerized multi-stage Docker deployment running on AWS ECS Fargate with managed PostgreSQL RDS and Redis caching.",
    "frontend_tech": "Next.js 15 (React 19), TypeScript, TailwindCSS, Zustand state management.",
    "backend_tech": "Python 3.12, FastAPI, LangGraph 0.2+, Pydantic v2, AsyncIO.",
    "database_choice": "PostgreSQL 16 for ACID compliance + Redis 7 for high-speed state caching.",
    "architecture_pattern": "Event-driven multi-agent sub-graph orchestration with state persistence.",
    "architectural_rationale": "Ensures modular separation of departmental concerns while allowing centralized orchestrator state updates.",
    "hiring_timeline_description": "Phase 1 (Month 1): Lead Agent Engineer & Senior Fullstack Dev. Phase 2 (Month 2): Tech Lead & Product Designer.",
    "category": "Cloud Infrastructure & LLM API Subscriptions",
    "details": "AWS Fargate, RDS PostgreSQL, Redis cluster, and model API usage budgets.",
    "mitigation_strategy": "Implement automated zero-trust data anonymization, explicit opt-in consent flows, and user data deletion APIs.",
    "requirement_name": "GDPR Right to Erasure & CCPA Data Privacy Protocol",
    "implementation_details": "Cascade deletion endpoint purging all org_sessions and chat telemetry upon user account deletion request."
}

def mock_generate_value(field_type: Any, field_name: str, prompt_text: str = "") -> Any:
    """
    Recursively builds realistic, domain-rich sample values for Pydantic fields.
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
            if "endpoint" in field_name or "api" in field_name:
                return [
                    "POST /api/v1/simulation/start - Trigger corporate workflow",
                    "GET /api/v1/simulation/{session_id}/status - Monitor state & logs",
                    "POST /api/v1/simulation/{session_id}/approve - Human-in-the-loop checkpoint"
                ]
            elif "driver" in field_name or "trend" in field_name:
                return [
                    "Enterprise demand for autonomous workflow automation",
                    "Shift towards modular multi-agent graph architectures (LangGraph)",
                    "Strict data privacy regulations requiring on-premise execution"
                ]
            elif "metric" in field_name or "kpi" in field_name:
                return [
                    "Workflow completion rate > 98%",
                    "Inter-departmental state sync latency < 150ms",
                    "Zero critic rejection loop deadlocks"
                ]
            elif "exclusion" in field_name or "out_of_scope" in field_name:
                return [
                    "Legacy monolith database migration (Post-MVP)",
                    "Custom physical hardware hardware integrations"
                ]
            elif "phase" in field_name or "roadmap" in field_name:
                return [
                    "Phase 1: Subgraph architecture & state schema initialization",
                    "Phase 2: Critic evaluation loops & guardrails setup",
                    "Phase 3: Multi-channel UI & executive report exports"
                ]
            elif "skill" in field_name:
                return ["Python / AsyncIO", "LangGraph / LangChain", "FastAPI / Pydantic v2", "Docker / Cloud Architecture"]
            elif "guideline" in field_name or "disclaimer" in field_name:
                return [
                    "All agent actions are corporate simulation scenarios for strategic planning.",
                    "No financial commitments or legal contracts are executed automatically without human signoff."
                ]
            return ["Enterprise Strategy", "Autonomous Agent Subgraphs", "Production Guardrails"]

    # Dict type
    if origin is dict or origin is Dict or "dict" in str(field_type).lower():
        return {"status": "validated", "tier": "enterprise", "execution_mode": "autonomous"}

    # String type check FIRST
    if field_type == str or "str" in str(field_type).lower():
        if field_name in DOMAIN_FIELD_DEFAULTS:
            return DOMAIN_FIELD_DEFAULTS[field_name]
        elif "name" in field_name or "title" in field_name:
            if "role" in field_name or "title" in field_name:
                return "Lead AI Agent & Systems Architect"
            elif "segment" in field_name or "persona" in field_name:
                return "Enterprise Product & Operations Managers"
            elif "tier" in field_name:
                return "Enterprise Pro Scale"
            elif "competitor" in field_name or "name" in field_name:
                return "AgentCorp Systems Inc."
            return "Enterprise Core System"
        elif "description" in field_name or "summary" in field_name or "rationale" in field_name or "vision" in field_name:
            return f"Comprehensive production definition for {field_name.replace('_', ' ')} tailored to enterprise automation."
        elif "risk" in field_name or "level" in field_name or "priority" in field_name:
            return "High"
        elif "salary" in field_name:
            return "$140,000 - $170,000 USD / year"
        return f"Production-grade {field_name.replace('_', ' ')} specification."
        
    # Numeric and Boolean types
    if field_type == bool or "bool" in str(field_type).lower():
        return True
    elif "score" in field_name or "rating" in field_name:
        return 9
    elif "count" in field_name or "headcount" in field_name or "weeks" in field_name or "months" in field_name or "retries" in field_name:
        return 12 if "count" in field_name else 6
    elif field_type == float or "float" in str(field_type).lower():
        if "share" in field_name:
            return 28.5
        elif "cost" in field_name or "burn" in field_name or "price" in field_name or "capital" in field_name:
            return 18500.0 if "burn" in field_name else (250000.0 if "capital" in field_name else 199.0)
        return 95.0
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
        google_key = settings.get_effective_google_api_key()
        if google_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                logger.info(f"Using live ChatGoogleGenerativeAI with model {self.default_model}")
                return ChatGoogleGenerativeAI(
                    model=self.default_model if "gemini" in self.default_model else "gemini-1.5-pro",
                    google_api_key=google_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.warning(f"Could not initialize ChatGoogleGenerativeAI: {e}. Falling back to MockChatModel.")
        
        openai_key = settings.get_effective_openai_api_key()
        if openai_key:
            try:
                from langchain_openai import ChatOpenAI
                logger.info(f"Using live ChatOpenAI with model gpt-4o")
                return ChatOpenAI(
                    model="gpt-4o" if "gpt" not in self.default_model else self.default_model,
                    api_key=openai_key,
                    temperature=self.temperature
                )
            except Exception as e:
                logger.warning(f"Could not initialize ChatOpenAI: {e}. Falling back to MockChatModel.")

        # Default fallback for testing and sandbox execution
        return MockChatModel()

llm_service = LLMService()
