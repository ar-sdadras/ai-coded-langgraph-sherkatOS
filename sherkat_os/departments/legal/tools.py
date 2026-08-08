from langchain_core.tools import tool

@tool
def calculate_risk_exposure(vulnerabilities_count: int, compliance_failures: int) -> str:
    """
    [Custom Tool] Calculates compliance risk factor.
    """
    risk = (vulnerabilities_count * 1.5) + (compliance_failures * 3.0)
    return f"Compliance Risk Exposure Factor: {risk:.2f}"

@tool
def generate_privacy_policy_stub(company_name: str, user_data_types: list[str]) -> str:
    """
    [Custom Tool] Generates privacy policy stubs.
    """
    data_str = ", ".join(user_data_types)
    return f"Privacy policy stub for {company_name}: We process {data_str}. Data stored encrypted."

@tool
def legal_db_search(jurisdiction: str, keyword: str) -> str:
    """
    [Built-in Tool] Run database lookup for legal codes.
    """
    return f"Legal lookup for '{keyword}' in jurisdiction '{jurisdiction}' completed."

@tool
def mcp_github_create_or_update_file(path: str, content: str) -> str:
    """
    [MCP Tool] Commit file to repo.
    """
    return f"File updated at repository path '{path}'."

legal_tools = [
    calculate_risk_exposure,
    generate_privacy_policy_stub,
    legal_db_search,
    mcp_github_create_or_update_file
]
