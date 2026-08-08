import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.departments.market.schemas import MarketAnalysisReport
from sherkat_os.departments.market.prompts import MARKET_ANALYST_PROMPT
from sherkat_os.services.logger import logger
from sherkat_os.services.llm import llm_service

async def market_analyst_node(state: MarketState) -> MarketState:
    raw_data = state.get("raw_research_data") or {}
    product_idea = state.get("product_idea", "Corporate AI Orchestration Sandbox")
    critic_feedback = state.get("critic_feedback")
    
    prompt = f"Product Idea: {product_idea}\nRaw Research Data: {json.dumps(raw_data)}"
    action_desc = "Synthesizing raw research into structured MarketAnalysisReport"
    if critic_feedback:
        prompt += f"\n\nCRITIC REFINEMENT DIRECTIVE: {critic_feedback}"
        action_desc = "Applying critic feedback refinement"

    model = llm_service.get_model()
    structured_model = model.with_structured_output(MarketAnalysisReport)
    
    with logger.status("Market Analyst", action_desc):
        report_obj: MarketAnalysisReport = await structured_model.ainvoke([
            SystemMessage(content=MARKET_ANALYST_PROMPT),
            HumanMessage(content=prompt)
        ])
    
    report_dict = report_obj.model_dump()
    msg = AIMessage(content=f"Generated Market Analysis Report (Viability Score: {report_obj.overall_viability_score}/10).")
    
    return {
        **state,
        "market_report": report_dict,
        "messages": [msg]
    }
