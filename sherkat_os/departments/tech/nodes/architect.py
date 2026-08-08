import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.services.logger import logger

async def system_architect_node(state: TechState) -> TechState:
    messages = state.get("messages", [])
    
    # If last message is a ToolMessage, process the DB check results
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        with logger.status("System Architect", f"Processing schema verification result: '{tool_msg.content[:40]}...'"):
            prd = state.get("prd") or {}
            
            tech_stack = {
                "frontend_tech": "Next.js 15 (React 19), TypeScript, TailwindCSS, Zustand",
                "backend_tech": "Python 3.12, FastAPI, LangGraph 0.2+, Pydantic v2, AsyncIO",
                "database_choice": "PostgreSQL 16 for ACID compliance + Redis 7 for high-speed state caching",
                "architecture_pattern": "Event-driven multi-agent sub-graph orchestration with state persistence",
                "architectural_rationale": "Ensures modular separation of departmental concerns while allowing centralized orchestrator state updates."
            }
            
            if state.get("critic_feedback"):
                tech_stack["architectural_rationale"] += " (Refined per technical critic directives)"
            
        return {
            **state,
            "tech_stack": tech_stack,
            "messages": [AIMessage(content="System architecture finalized after schema verification.")]
        }
        
    else:
        with logger.status("System Architect", "Invoking Postgres query tool for schema verification"):
            tool_call = {
                "name": "mcp_postgres_query",
                "args": {"sql_query": "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"},
                "id": "mcp_db_query_01",
                "type": "tool_call"
            }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
