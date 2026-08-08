import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.product.state import ProductState
from sherkat_os.departments.product.schemas import ProductRequirementDocument
from sherkat_os.departments.product.prompts import PRODUCT_WRITER_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def product_writer_node(state: ProductState) -> ProductState:
    logger.log_node_start("Product Writer", "Synthesizing market analysis into ProductRequirementDocument...")
    
    market_analysis = state.get("market_analysis") or {}
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"Market Analysis Input: {json.dumps(market_analysis)}"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        logger.log_node_start("Product Writer", "Refining PRD based on critic feedback...")

    model = llm_service.get_model()
    structured_model = model.with_structured_output(ProductRequirementDocument)
    
    prd_obj: ProductRequirementDocument = await structured_model.ainvoke([
        SystemMessage(content=PRODUCT_WRITER_PROMPT),
        HumanMessage(content=prompt)
    ])
    
    prd_dict = prd_obj.model_dump()
    msg = AIMessage(content="Generated Product Requirement Document (PRD).")
    
    return {
        **state,
        "prd_final": prd_dict,
        "messages": [msg]
    }
