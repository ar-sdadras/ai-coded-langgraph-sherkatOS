from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.tech.state import TechState
from sherkat_os.departments.tech.nodes.architect import system_architect_node
from sherkat_os.departments.tech.nodes.planner import technical_planner_node
from sherkat_os.departments.tech.nodes.critic import tech_critic_node
from sherkat_os.departments.tech.tools import tech_tools
from sherkat_os.config.settings import settings

tech_builder = StateGraph(TechState)

# Add Nodes
tech_builder.add_node("Architect", system_architect_node)
tech_builder.add_node("Planner", technical_planner_node)
tech_builder.add_node("Critic", tech_critic_node)
tech_builder.add_node("tools", ToolNode(tech_tools))

# Add Edges
tech_builder.add_edge(START, "Architect")
tech_builder.add_edge("tools", "Architect")  # Loop back

def route_architect(state: TechState) -> Literal["tools", "Planner"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Planner"

tech_builder.add_conditional_edges("Architect", route_architect)
tech_builder.add_edge("Planner", "Critic")

def route_tech_critic(state: TechState) -> Literal["Architect", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Architect"
        else:
            print("[Tech Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

tech_builder.add_conditional_edges("Critic", route_tech_critic)

tech_dept_graph = tech_builder.compile(checkpointer=MemorySaver())
