import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.legal.state import LegalState
from sherkat_os.departments.legal.schemas import LegalAudit
from sherkat_os.departments.legal.prompts import LEGAL_ADVISOR_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def legal_advisor_node(state: LegalState) -> LegalState:
    prd = state.get("prd") or {}
    tech_roadmap = state.get("tech_roadmap") or {}
    market_analysis = state.get("market_analysis") or {}
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"PRD: {json.dumps(prd)}\nTech Roadmap: {json.dumps(tech_roadmap)}\nMarket Analysis: {json.dumps(market_analysis)}"
    action_desc = "Synthesizing legal requirements into LegalAudit"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        action_desc = "Refining legal compliance audit based on critic feedback"

    model = llm_service.get_model()
    structured_model = model.with_structured_output(LegalAudit)
    
    with logger.status("Legal Advisor", action_desc):
        audit_obj: LegalAudit = await structured_model.ainvoke([
            SystemMessage(content=LEGAL_ADVISOR_PROMPT),
            HumanMessage(content=prompt)
        ])
    
    audit_dict = audit_obj.model_dump()
    msg = AIMessage(content="Generated Legal & Compliance Audit.")
    
    return {
        **state,
        "legal_compliance": audit_dict,
        "messages": [msg]
    }
