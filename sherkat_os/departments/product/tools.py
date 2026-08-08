from langchain_core.tools import tool

@tool
def calculate_complexity_multiplier(features_count: int, integrations_count: int) -> str:
    """
    [Custom Tool] Calculates complexity multiplier based on features and integrations.
    """
    multiplier = 1.0 + (features_count * 0.1) + (integrations_count * 0.2)
    return f"Complexity Multiplier: {multiplier:.2f}x"

@tool
def generate_user_story_template(role: str, action: str, benefit: str) -> str:
    """
    [Custom Tool] Generates a formatted user story.
    """
    return f"As a {role}, I want to {action} so that {benefit}."

@tool
def arxiv_search(query: str) -> str:
    """
    [Built-in Tool] Query Arxiv repository for product design papers.
    """
    return f"Arxiv Search: Document found: 'Design patterns for multi-agent human-in-the-loop systems' (2025)."

@tool
def mcp_stitch_create_project(name: str) -> str:
    """
    [MCP Tool: StitchMCP/create_project] Initialize a project layout in Stitch workspace.
    """
    return f"StitchMCP: Project '{name}' created with ID 'stitch_proj_98765'."

@tool
def mcp_stitch_create_design_system(project_id: str) -> str:
    """
    [MCP Tool: StitchMCP/create_design_system] Creates a design system for a project.
    """
    return f"StitchMCP: Design system initialized in project '{project_id}'."

product_tools = [
    calculate_complexity_multiplier,
    generate_user_story_template,
    arxiv_search,
    mcp_stitch_create_project,
    mcp_stitch_create_design_system
]
