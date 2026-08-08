from langchain_core.tools import tool

@tool
def benchmark_salary_by_role(role_title: str, experience_years: int) -> str:
    """
    [Custom Tool] Benchmarks base salary.
    """
    base = 80000 + (experience_years * 10000)
    if "lead" in role_title.lower():
        base += 20000
    return f"Benchmark base salary for {role_title} ({experience_years} yrs exp): ${base:,} USD."

@tool
def generate_job_description_boilerplate(role_title: str, core_stack: list[str]) -> str:
    """
    [Custom Tool] Generates description templates.
    """
    stack_str = ", ".join(core_stack)
    return f"JD Boilerplate for {role_title}: Looking for experts in {stack_str}. {experience_years if 'experience_years' in locals() else 4}+ years required."

@tool
def google_search_hiring_rates(query: str) -> str:
    """
    [Built-in Tool] Run search for standard hiring rates in SaaS.
    """
    return f"Hiring rates query '{query}' processed for recruitment benchmarking."

@tool
def mcp_github_add_team_member(team_id: str, username: str) -> str:
    """
    [MCP Tool] Adds team members to organization repository.
    """
    return f"User '{username}' assigned to team '{team_id}'."

hr_tools = [
    benchmark_salary_by_role,
    generate_job_description_boilerplate,
    google_search_hiring_rates,
    mcp_github_add_team_member
]
