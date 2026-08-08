import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.finance.state import FinanceState
from sherkat_os.services.logger import logger

async def finance_modeler_node(state: FinanceState) -> FinanceState:
    logger.log_node_start("Finance Modeler", "Synthesizing budget and pricing tiers...")
    
    draft = state.get("financial_draft") or {}
    
    financial_model = {
        "capital_requirement_usd": 250000.0,
        "monthly_burn_rate_usd": 17500.0,
        "operating_costs": [
            {"category": "Cloud Hosting", "estimated_monthly_cost": draft.get("monthly_infrastructure_cost", 2500.0), "details": "AWS ECS + RDS instances"},
            {"category": "Personnel", "estimated_monthly_cost": draft.get("monthly_labor_cost", 15000.0), "details": "Core engineering & operations staff"}
        ],
        "pricing_tiers": [
            {"name": "Standard", "price_usd": 49.0, "included_features": ["Up to 3 agent sub-graphs", "Standard dashboard"]},
            {"name": "Enterprise", "price_usd": 499.0, "included_features": ["Unlimited agent sub-graphs", "Dedicated checkpointer saver"]}
        ],
        "estimated_payback_period_months": 18
    }
    
    if state.get("critic_feedback"):
        logger.log_node_start("Finance Modeler", f"Refining financial model based on critic feedback: '{state['critic_feedback']}'")
        financial_model["pricing_tiers"].append(
            {"name": "Developer Sandbox", "price_usd": 0.0, "included_features": ["Local in-memory checkpointer testing only"]}
        )
        financial_model["capital_requirement_usd"] = 300000.0 # Adjusted for developer pipeline support
        
    msg = AIMessage(content=f"Generated financial plan: {json.dumps(financial_model)}")
    return {
        **state,
        "financial_model": financial_model,
        "messages": [msg]
    }
