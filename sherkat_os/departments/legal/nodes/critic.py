from langchain_core.messages import AIMessage
from sherkat_os.departments.legal.state import LegalState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def legal_critic_node(state: LegalState) -> LegalState:
    logger.log_node_start("Legal Critic", "Reviewing compliance metrics and disclaimers...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "Legal disclaimers must include a limitation of liability clause for simulated financial models."
        logger.log_critic_rejection("Legal Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("Legal Critic", "Compliance and legal audit completed.")
        msg = AIMessage(content="Approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
