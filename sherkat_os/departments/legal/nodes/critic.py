import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.legal.state import LegalState
from sherkat_os.departments.legal.schemas import CriticFeedback
from sherkat_os.departments.legal.prompts import LEGAL_CRITIC_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service
from sherkat_os.config.settings import settings

async def legal_critic_node(state: LegalState) -> LegalState:
    logger.log_node_start("Legal Critic", "Auditing Legal Compliance Framework...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    legal_compliance = state.get("legal_compliance") or {}
    
    model = llm_service.get_model()
    structured_model = model.with_structured_output(CriticFeedback)
    
    prompt = f"Legal Audit to Evaluate: {json.dumps(legal_compliance)}\nIteration: {current_retries + 1} of {max_retries}"
    eval_result: CriticFeedback = await structured_model.ainvoke([
        SystemMessage(content=LEGAL_CRITIC_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    if current_retries >= max_retries:
        eval_result.is_approved = True
        eval_result.feedback = "Max retries reached; approved with current legal compliance state."
        
    if not eval_result.is_approved:
        logger.log_critic_rejection("Legal Critic", eval_result.feedback, current_retries + 1, max_retries)
        feedback_str = eval_result.feedback
    else:
        logger.log_critic_approval("Legal Critic", eval_result.feedback)
        feedback_str = None

    return {
        **state,
        "critic_feedback": feedback_str,
        "retry_count": current_retries + 1,
        "messages": [AIMessage(content=f"Legal Critic Audit: {'Approved' if eval_result.is_approved else 'Refinement Required'}")]
    }
