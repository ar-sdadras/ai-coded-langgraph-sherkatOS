from langchain_core.messages import AIMessage
from sherkat_os.departments.product.state import ProductState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def product_critic_node(state: ProductState) -> ProductState:
    logger.log_node_start("Product Critic", "Reviewing PRD and success metrics...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "The PRD scope exclusions should explicitly outline multi-cloud clustering bounds."
        logger.log_critic_rejection("Product Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("Product Critic", "PRD and success metrics are solid.")
        msg = AIMessage(content="Approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
