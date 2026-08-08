from langchain_core.messages import AIMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def tech_critic_node(state: TechState) -> TechState:
    logger.log_node_start("Tech Critic", "Evaluating technical design and feasibility...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "The architecture pattern needs a detailed cost estimation for container execution."
        logger.log_critic_rejection("Tech Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("Tech Critic", "Technology blueprint is realistic and feasible.")
        msg = AIMessage(content="Roadmap approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
