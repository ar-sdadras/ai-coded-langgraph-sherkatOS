import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.product.state import ProductState
from sherkat_os.departments.product.schemas import CriticFeedback
from sherkat_os.departments.product.prompts import PRODUCT_CRITIC_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service
from sherkat_os.config.settings import settings

async def product_critic_node(state: ProductState) -> ProductState:
    current_retries = state.get("retry_count", 0)
    max_retries = settings.max_retries
    prd_final = state.get("prd_final") or {}
    
    model = llm_service.get_model()
    structured_model = model.with_structured_output(CriticFeedback)
    
    prompt = f"PRD to Audit: {json.dumps(prd_final)}\nIteration: {current_retries + 1} of {max_retries}"
    
    with logger.status("Product Critic", f"Auditing PRD (Iteration {current_retries + 1}/{max_retries})"):
        eval_result: CriticFeedback = await structured_model.ainvoke([
            SystemMessage(content=PRODUCT_CRITIC_PROMPT),
            HumanMessage(content=prompt)
        ])
    
    if current_retries >= max_retries:
        eval_result.is_approved = True
        eval_result.feedback = "Max retries reached; approved with current PRD state."
        
    if not eval_result.is_approved:
        logger.log_critic_rejection("Product Critic", eval_result.feedback, current_retries + 1, max_retries)
        feedback_str = eval_result.feedback
    else:
        logger.log_critic_approval("Product Critic", eval_result.feedback)
        feedback_str = None

    return {
        **state,
        "critic_feedback": feedback_str,
        "retry_count": current_retries + 1,
        "messages": [AIMessage(content=f"Product Critic Audit: {'Approved' if eval_result.is_approved else 'Refinement Required'}")]
    }
