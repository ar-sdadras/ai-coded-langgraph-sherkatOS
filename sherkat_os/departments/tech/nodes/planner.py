import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.services.logger import logger

async def technical_planner_node(state: TechState) -> TechState:
    tech_stack = state.get("tech_stack") or {}
    logger.log_node_start("Technical Planner", f"Drafting implementation plan based on stack: {tech_stack.get('backend_tech')}")
    
    blueprint = {
        "database_schema_concept": "Table: org_states, Table: agent_messages, Table: runs",
        "core_api_endpoints": [
            {"method": "POST", "path": "/api/v1/run", "description": "Trigger an autonomous simulation run."},
            {"method": "GET", "path": "/api/v1/run/{id}/status", "description": "Check run state and messages."}
        ],
        "infrastructure_and_deployment": "Dockerized container on AWS ECS Fargate, managed PostgreSQL RDS",
        "mvp_roadmap_phases": ["Phase 1: Sub-graph definition and State orchestration", "Phase 2: API integration"]
    }
    
    msg = AIMessage(content=f"Created blueprint: {json.dumps(blueprint)}")
    return {
        **state,
        "tech_blueprint": blueprint,
        "messages": [msg]
    }
