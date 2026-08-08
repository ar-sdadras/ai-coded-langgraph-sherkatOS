from langchain_core.messages import AIMessage
from sherkat_os.departments.hr.state import HRState
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings

async def hr_critic_node(state: HRState) -> HRState:
    logger.log_node_start("HR Critic", "Reviewing roles, salary ranges, and hiring pipeline...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    
    if current_retries == 0:
        feedback = "Staffing plan lacks a part-time UI/UX designer role to support Next.js frontend design."
        logger.log_critic_rejection("HR Critic", feedback, current_retries + 1, max_retries)
        msg = AIMessage(content=f"Feedback: {feedback}")
    else:
        feedback = None
        logger.log_critic_approval("HR Critic", "Operational staffing strategy is clear.")
        msg = AIMessage(content="Approved.")
        
    return {
        **state,
        "critic_feedback": feedback,
        "retry_count": current_retries + 1,
        "messages": [msg]
    }
