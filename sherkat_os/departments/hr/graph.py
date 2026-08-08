from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.hr.state import HRState
from sherkat_os.departments.hr.nodes.recruiter import hr_recruiter_node
from sherkat_os.departments.hr.nodes.planner import hr_planner_node
from sherkat_os.departments.hr.nodes.critic import hr_critic_node
from sherkat_os.departments.hr.tools import hr_tools
from sherkat_os.config.settings import settings

hr_builder = StateGraph(HRState)

# Add Nodes
hr_builder.add_node("Recruiter", hr_recruiter_node)
hr_builder.add_node("Planner", hr_planner_node)
hr_builder.add_node("Critic", hr_critic_node)
hr_builder.add_node("tools", ToolNode(hr_tools))

# Add Edges
hr_builder.add_edge(START, "Recruiter")
hr_builder.add_edge("tools", "Recruiter")  # Loop back

def route_recruiter(state: HRState) -> Literal["tools", "Planner"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Planner"

hr_builder.add_conditional_edges("Recruiter", route_recruiter)
hr_builder.add_edge("Planner", "Critic")

def route_hr_critic(state: HRState) -> Literal["Planner", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Planner"
        else:
            print("[HR Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

hr_builder.add_conditional_edges("Critic", route_hr_critic)

hr_dept_graph = hr_builder.compile(checkpointer=MemorySaver())
