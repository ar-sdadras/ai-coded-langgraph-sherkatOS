import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.finance.state import FinanceState
from sherkat_os.departments.finance.schemas import FinancialPlan
from sherkat_os.departments.finance.prompts import FINANCE_MODELER_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def finance_modeler_node(state: FinanceState) -> FinanceState:
    prd = state.get("prd") or {}
    tech_roadmap = state.get("tech_roadmap") or {}
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"PRD: {json.dumps(prd)}\nTech Roadmap: {json.dumps(tech_roadmap)}"
    action_desc = "Synthesizing unit economics and FinancialPlan"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        action_desc = "Refining financial plan based on critic feedback"

    model = llm_service.get_model()
    structured_model = model.with_structured_output(FinancialPlan)
    
    with logger.status("Finance Modeler", action_desc):
        plan_obj: FinancialPlan = await structured_model.ainvoke([
            SystemMessage(content=FINANCE_MODELER_PROMPT),
            HumanMessage(content=prompt)
        ])
    
    plan_dict = plan_obj.model_dump()
    msg = AIMessage(content="Generated Corporate Financial Plan.")
    
    return {
        **state,
        "financial_model": plan_dict,
        "messages": [msg]
    }
