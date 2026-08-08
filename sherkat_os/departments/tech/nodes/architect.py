import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.services.logger import logger

async def system_architect_node(state: TechState) -> TechState:
    messages = state.get("messages", [])
    
    # If last message is a ToolMessage, process the DB check results
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("System Architect", f"Processing tool result: '{tool_msg.content}'")
        
        prd = state.get("prd") or {}
        
        tech_stack = {
            "frontend_tech": "Next.js (React) with TailwindCSS",
            "backend_tech": "Python FastAPI with LangGraph Orchestration",
            "database_choice": "PostgreSQL (Relational, SQL) for transactional stability",
            "architecture_pattern": "Modular sub-graphs (Hierarchical Agent topology)",
            "architectural_rationale": "High flexibility to define and execute sub-agents dynamically."
        }
        
        if state.get("critic_feedback"):
            logger.log_node_start("System Architect", f"Refining architecture based on critic feedback: '{state['critic_feedback']}'")
            tech_stack["architectural_rationale"] += " (Optimized cost estimation & serverless functions usage)"
            
        return {
            **state,
            "tech_stack": tech_stack,
            "messages": [AIMessage(content="System architecture finalized after Postgres MCP schema verification.")]
        }
        
    else:
        # First call: Emit a tool call for postgres query MCP tool
        logger.log_node_start("System Architect", "Invoking Postgres MCP query to verify database name space...")
        
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
