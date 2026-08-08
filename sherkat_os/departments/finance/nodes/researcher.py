import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.finance.state import FinanceState
from sherkat_os.services.logger import logger

async def finance_researcher_node(state: FinanceState) -> FinanceState:
    messages = state.get("messages", [])
    
    # If last message is a ToolMessage, process the financial tool output
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("Finance Researcher", f"Processing tool result: '{tool_msg.content}'")
        
        draft = {
            "monthly_infrastructure_cost": 2500.0,
            "monthly_labor_cost": 15000.0,
            "pricing": [
                {"tier": "Standard", "rate": 49.0},
                {"tier": "Enterprise", "rate": 499.0}
            ],
            "breakeven_calculation": tool_msg.content
        }
        
        return {
            **state,
            "financial_draft": draft,
            "messages": [AIMessage(content="Finance research parameters established after payback analysis.")]
        }
        
    else:
        # First call: Emit a tool call for custom break-even months tool
        logger.log_node_start("Finance Researcher", "Calculating break-even projections using custom tool...")
        
        tool_call = {
            "name": "calculate_breakeven_months",
            "args": {"monthly_burn": 17500.0, "avg_price_per_user": 49.0, "target_customers": 500},
            "id": "calc_breakeven_01",
            "type": "tool_call"
        }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
