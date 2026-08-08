from langchain_core.tools import tool

@tool
def calculate_infrastructure_capacity(daily_active_users: int, queries_per_second: float) -> str:
    """
    [Custom Tool] Calculates estimated database queries capacity.
    """
    total_qpd = daily_active_users * queries_per_second * 10
    return f"Estimated infrastructure capacity: {total_qpd:.0f} queries/day capacity required."

@tool
def check_api_compliance(endpoint_path: str, method: str) -> str:
    """
    [Custom Tool] Checks path and method compliance.
    """
    is_valid = endpoint_path.startswith("/api/v1/")
    return f"API Endpoint compliance for {method} {endpoint_path}: {'Compliant' if is_valid else 'Non-compliant path structure'}"

@tool
def shell_command_validator(cmd: str) -> str:
    """
    [Built-in Tool] Validates CLI build commands for correctness.
    """
    return f"Shell Validator: Command '{cmd}' validated for container execution."

@tool
def mcp_github_create_pull_request(repo: str, branch: str, title: str) -> str:
    """
    [MCP Tool] Create a PR for the repository.
    """
    return f"Pull Request '{title}' created on branch '{branch}' in repository '{repo}'."

@tool
def mcp_postgres_query(sql_query: str) -> str:
    """
    [MCP Tool] Run query on postgres database schema metadata.
    """
    return f"Schema query '{sql_query}' executed successfully."

tech_tools = [
    calculate_infrastructure_capacity,
    check_api_compliance,
    shell_command_validator,
    mcp_github_create_pull_request,
    mcp_postgres_query
]
