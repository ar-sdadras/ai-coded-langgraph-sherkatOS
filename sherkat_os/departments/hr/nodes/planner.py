import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.hr.state import HRState
from sherkat_os.departments.hr.schemas import HRStaffingPlan
from sherkat_os.departments.hr.prompts import HR_PLANNER_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def hr_planner_node(state: HRState) -> HRState:
    logger.log_node_start("HR Planner", "Synthesizing staffing requirements into HRStaffingPlan...")
    
    prd = state.get("prd") or {}
    financial_model = state.get("financial_model") or {}
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"PRD: {json.dumps(prd)}\nFinancial Model: {json.dumps(financial_model)}"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        logger.log_node_start("HR Planner", "Refining HR plan based on critic feedback...")

    model = llm_service.get_model()
    structured_model = model.with_structured_output(HRStaffingPlan)
    
    plan_obj: HRStaffingPlan = await structured_model.ainvoke([
        SystemMessage(content=HR_PLANNER_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    plan_dict = plan_obj.model_dump()
    msg = AIMessage(content="Generated HR & Operations Staffing Plan.")
    
    return {
        **state,
        "hr_plan": plan_dict,
        "messages": [msg]
    }
