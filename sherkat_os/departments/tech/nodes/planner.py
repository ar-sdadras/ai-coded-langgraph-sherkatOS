import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.departments.tech.schemas import TechnicalBlueprint
from sherkat_os.departments.tech.prompts import TECH_PLANNER_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def technical_planner_node(state: TechState) -> TechState:
    prd = state.get("prd") or {}
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"Product Requirements Document (PRD): {json.dumps(prd)}"
    action_desc = "Synthesizing PRD into TechnicalBlueprint"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        action_desc = "Refining technical blueprint based on critic feedback"

    model = llm_service.get_model()
    structured_model = model.with_structured_output(TechnicalBlueprint)
    
    with logger.status("Technical Planner", action_desc):
        blueprint_obj: TechnicalBlueprint = await structured_model.ainvoke([
            SystemMessage(content=TECH_PLANNER_PROMPT),
            HumanMessage(content=prompt)
        ])
    
    blueprint_dict = blueprint_obj.model_dump()
    msg = AIMessage(content="Generated Technical Blueprint & Architecture Roadmap.")
    
    return {
        **state,
        "tech_blueprint": blueprint_dict,
        "messages": [msg]
    }
