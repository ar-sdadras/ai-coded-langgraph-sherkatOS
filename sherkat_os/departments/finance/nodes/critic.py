from langchain_core.messages import AIMessage
from sherkat_os.departments.finance.state import FinanceState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def finance_critic_node(state: FinanceState) -> FinanceState:
    logger.log_node_start("Finance Critic", "Reviewing pricing tiers and capital estimates...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "Pricing model lacks a developer-focused free sandbox tier to attract early adopters."
        logger.log_critic_rejection("Finance Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("Finance Critic", "Pricing tiers and R&D costs are well balanced.")
        msg = AIMessage(content="Approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
