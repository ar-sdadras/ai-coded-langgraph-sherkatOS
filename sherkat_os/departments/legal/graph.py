from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.legal.state import LegalState
from sherkat_os.departments.legal.nodes.auditor import legal_auditor_node
from sherkat_os.departments.legal.nodes.advisor import legal_advisor_node
from sherkat_os.departments.legal.nodes.critic import legal_critic_node
from sherkat_os.departments.legal.tools import legal_tools
from sherkat_os.config.settings import settings

legal_builder = StateGraph(LegalState)

# Add Nodes
legal_builder.add_node("Auditor", legal_auditor_node)
legal_builder.add_node("Advisor", legal_advisor_node)
legal_builder.add_node("Critic", legal_critic_node)
legal_builder.add_node("tools", ToolNode(legal_tools))

# Add Edges
legal_builder.add_edge(START, "Auditor")
legal_builder.add_edge("tools", "Auditor")  # Loop back

def route_auditor(state: LegalState) -> Literal["tools", "Advisor"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Advisor"

legal_builder.add_conditional_edges("Auditor", route_auditor)
legal_builder.add_edge("Advisor", "Critic")

def route_legal_critic(state: LegalState) -> Literal["Advisor", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Advisor"
        else:
            print("[Legal Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

legal_builder.add_conditional_edges("Critic", route_legal_critic)

legal_dept_graph = legal_builder.compile(checkpointer=MemorySaver())
