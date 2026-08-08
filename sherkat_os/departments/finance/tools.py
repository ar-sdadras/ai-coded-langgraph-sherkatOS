from langchain_core.tools import tool

@tool
def calculate_breakeven_months(monthly_burn: float, avg_price_per_user: float, target_customers: int) -> str:
    """
    [Custom Tool] Calculates months needed to reach break-even.
    """
    monthly_revenue = avg_price_per_user * target_customers
    if monthly_revenue <= monthly_burn:
        return "Break-even is unreachable with current customer targets."
    months = (monthly_burn * 12) / (monthly_revenue - monthly_burn)
    return f"Calculated break-even payback period: {months:.1f} months."

@tool
def project_revenue_growth(starting_mrr: float, growth_rate: float, months: int) -> str:
    """
    [Custom Tool] Projects MRR growth.
    """
    ending_mrr = starting_mrr * ((1.0 + growth_rate) ** months)
    return f"Projected MRR after {months} months: ${ending_mrr:.2f}"

@tool
def math_calculator(expression: str) -> str:
    """
    [Built-in Tool] Run simple math calculator.
    """
    try:
        val = eval(expression, {"__builtins__": None}, {})
        return f"Math Calculator: Result is {val}"
    except Exception as e:
        return f"Math Calculator Error: {str(e)}"

@tool
def mcp_n8n_create_workflow(name: str, nodes_config: str) -> str:
    """
    [MCP Tool: mcp-docker-toolkit/n8n_create_workflow] Creates financial automation workflow.
    """
    return f"n8n MCP: Successfully created workflow '{name}' for financial payout automation."

finance_tools = [
    calculate_breakeven_months,
    project_revenue_growth,
    math_calculator,
    mcp_n8n_create_workflow
]
