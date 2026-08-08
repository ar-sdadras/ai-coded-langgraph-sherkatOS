import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.tech.state import TechState
from sherkat_os.departments.tech.schemas import CriticFeedback
from sherkat_os.departments.tech.prompts import TECH_CRITIC_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service
from sherkat_os.config.settings import settings

async def tech_critic_node(state: TechState) -> TechState:
    logger.log_node_start("Tech Critic", "Performing technical architectural audit...")
    
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    tech_blueprint = state.get("tech_blueprint") or {}
    
    model = llm_service.get_model()
    structured_model = model.with_structured_output(CriticFeedback)
    
    prompt = f"Technical Blueprint to Audit: {json.dumps(tech_blueprint)}\nIteration: {current_retries + 1} of {max_retries}"
    eval_result: CriticFeedback = await structured_model.ainvoke([
        SystemMessage(content=TECH_CRITIC_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    if current_retries >= max_retries:
        eval_result.is_approved = True
        eval_result.feedback = "Max retries reached; approved with current technical blueprint state."
        
    if not eval_result.is_approved:
        logger.log_critic_rejection("Tech Critic", eval_result.feedback, current_retries + 1, max_retries)
        feedback_str = eval_result.feedback
    else:
        logger.log_critic_approval("Tech Critic", eval_result.feedback)
        feedback_str = None

    return {
        **state,
        "critic_feedback": feedback_str,
        "retry_count": current_retries + 1,
        "messages": [AIMessage(content=f"Tech Critic Audit: {'Approved' if eval_result.is_approved else 'Refinement Required'}")]
    }
