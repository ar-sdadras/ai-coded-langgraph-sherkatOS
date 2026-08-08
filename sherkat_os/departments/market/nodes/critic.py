import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.departments.market.schemas import CriticFeedback
from sherkat_os.departments.market.prompts import MARKET_CRITIC_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service
from sherkat_os.config.settings import settings

async def market_critic_node(state: MarketState) -> MarketState:
    logger.log_node_start("Market Critic", "Performing quality audit on Market Analysis Report...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    market_report = state.get("market_report") or {}
    
    model = llm_service.get_model()
    structured_model = model.with_structured_output(CriticFeedback)
    
    prompt = f"Market Report to Audit: {json.dumps(market_report)}\nIteration: {current_retries + 1} of {max_retries}"
    eval_result: CriticFeedback = await structured_model.ainvoke([
        SystemMessage(content=MARKET_CRITIC_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    # Force pass if max retries reached to prevent infinite loops
    if current_retries >= max_retries:
        eval_result.is_approved = True
        eval_result.feedback = "Max retries reached; approved with current report state."
        
    if not eval_result.is_approved:
        logger.log_critic_rejection("Market Critic", eval_result.feedback, current_retries + 1, max_retries)
        feedback_str = eval_result.feedback
    else:
        logger.log_critic_approval("Market Critic", eval_result.feedback)
        feedback_str = None

    return {
        **state,
        "critic_feedback": feedback_str,
        "retry_count": current_retries + 1,
        "messages": [AIMessage(content=f"Market Critic Audit: {'Approved' if eval_result.is_approved else 'Refinement Required'}")]
    }
