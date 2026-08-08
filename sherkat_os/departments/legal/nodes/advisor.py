import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.legal.state import LegalState
from sherkat_os.services.logger import logger

async def legal_advisor_node(state: LegalState) -> LegalState:
    logger.log_node_start("Legal Advisor", "Compiling compliance audit and terms of service guidelines...")
    
    draft = state.get("legal_draft") or {}
    
    legal_compliance = {
        "compliance_risks": [
            {
                "area": risk["area"],
                "risk_level": risk["level"],
                "mitigation_strategy": risk["mitigation"]
            } for risk in draft.get("risks", [])
        ],
        "privacy_requirements": [
            {
                "requirement_name": req["name"],
                "implementation_details": req["details"]
            } for req in draft.get("privacy", [])
        ],
        "terms_of_service_guidelines": [
            "Users must acknowledge that simulated agent actions do not represent actual company decisions.",
            "All test outputs are sandbox environments."
        ],
        "disclaimer_requirements": [
            "SherkatOS is an AI simulator. All simulation events, transactions, and hires are fictitious."
        ]
    }
    
    if state.get("critic_feedback"):
        logger.log_node_start("Legal Advisor", f"Refining compliance audit based on critic feedback: '{state['critic_feedback']}'")
        legal_compliance["disclaimer_requirements"].append(
            "Limitation of Liability: No warranty is made regarding the accuracy of simulated financial models."
        )
        
    msg = AIMessage(content=f"Generated Legal Audit: {json.dumps(legal_compliance)}")
    return {
        **state,
        "legal_compliance": legal_compliance,
        "messages": [msg]
    }
