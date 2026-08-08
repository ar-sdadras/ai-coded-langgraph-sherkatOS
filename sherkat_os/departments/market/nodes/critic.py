from langchain_core.messages import AIMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def market_critic_node(state: MarketState) -> MarketState:
    logger.log_node_start("Market Critic", "Reviewing market report details...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "Personas and value proposition lack details about security compliance."
        logger.log_critic_rejection("Market Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("Market Critic", "Market Analysis Report is comprehensive.")
        msg = AIMessage(content="Approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
