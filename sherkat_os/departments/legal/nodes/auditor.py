import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.legal.state import LegalState
from sherkat_os.services.logger import logger

async def legal_auditor_node(state: LegalState) -> LegalState:
    messages = state.get("messages", [])
    
    # If last message is a ToolMessage, process the compliance audit output
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("Legal Auditor", f"Processing tool result: '{tool_msg.content}'")
        
        draft = {
            "risks": [
                {
                    "area": "GDPR Compliance",
                    "level": "High",
                    "mitigation": "Store personal data encrypted; implement data deletion endpoint."
                }
            ],
            "privacy": [
                {
                    "name": "Right to be Forgotten",
                    "details": "Trigger cascade delete on org_states and agent_messages for user session."
                }
            ],
            "risk_score_calculation": tool_msg.content
        }
        
        return {
            **state,
            "legal_draft": draft,
            "messages": [AIMessage(content="Legal and regulatory risks drafted after exposure analysis.")]
        }
        
    else:
        # First call: Emit a tool call for custom risk exposure tool
        logger.log_node_start("Legal Auditor", "Calculating compliance risk exposure factor...")
        
        tool_call = {
            "name": "calculate_risk_exposure",
            "args": {"vulnerabilities_count": 3, "compliance_failures": 1},
            "id": "calc_risk_01",
            "type": "tool_call"
        }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
