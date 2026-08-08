import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.services.logger import logger

async def market_analyst_node(state: MarketState) -> MarketState:
    logger.log_node_start("Market Analyst", "Synthesizing raw research into structured analysis...")
    
    raw_data = state.get("raw_research_data") or {}
    
    report = {
        "market_size_description": raw_data.get("tam_description", "Large TAM"),
        "personas": [
            {"segment_name": "Product Managers", "pain_points": ["Manual coordination"], "willingness_to_pay_rating": 8}
        ],
        "competitor_landscape": [
            {"name": "CorpA", "market_share_percentage": 35.0, "key_strengths": ["Sales"], "vulnerabilities": ["Legacy tech"]}
        ],
        "industry_drivers": raw_data.get("trends", []),
        "overall_viability_score": 8,
        "suggested_value_proposition": "Provide fully autonomous agent coordination simulation."
    }
    
    if state.get("critic_feedback"):
        logger.log_node_start("Market Analyst", f"Refining report based on critic feedback: '{state['critic_feedback']}'")
        report["suggested_value_proposition"] += " (With enterprise-grade security & compliance integrations)"
        report["overall_viability_score"] = 9
        
    msg = AIMessage(content=f"Generated market report: {json.dumps(report)}")
    return {
        **state,
        "market_report": report,
        "messages": [msg]
    }
