from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.finance.state import FinanceState
from sherkat_os.departments.finance.nodes.researcher import finance_researcher_node
from sherkat_os.departments.finance.nodes.modeler import finance_modeler_node
from sherkat_os.departments.finance.nodes.critic import finance_critic_node
from sherkat_os.departments.finance.tools import finance_tools
from sherkat_os.config.settings import settings

finance_builder = StateGraph(FinanceState)

# Add Nodes
finance_builder.add_node("Researcher", finance_researcher_node)
finance_builder.add_node("Modeler", finance_modeler_node)
finance_builder.add_node("Critic", finance_critic_node)
finance_builder.add_node("tools", ToolNode(finance_tools))

# Add Edges
finance_builder.add_edge(START, "Researcher")
finance_builder.add_edge("tools", "Researcher")  # Loop back

def route_researcher(state: FinanceState) -> Literal["tools", "Modeler"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Modeler"

finance_builder.add_conditional_edges("Researcher", route_researcher)
finance_builder.add_edge("Modeler", "Critic")

def route_finance_critic(state: FinanceState) -> Literal["Modeler", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Modeler"
        else:
            print("[Finance Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

finance_builder.add_conditional_edges("Critic", route_finance_critic)

finance_dept_graph = finance_builder.compile(checkpointer=MemorySaver())
