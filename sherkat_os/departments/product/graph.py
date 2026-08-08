from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.product.state import ProductState
from sherkat_os.departments.product.nodes.researcher import product_researcher_node
from sherkat_os.departments.product.nodes.writer import product_writer_node
from sherkat_os.departments.product.nodes.critic import product_critic_node
from sherkat_os.departments.product.tools import product_tools
from sherkat_os.config.settings import settings

product_builder = StateGraph(ProductState)

# Add Nodes
product_builder.add_node("Researcher", product_researcher_node)
product_builder.add_node("Writer", product_writer_node)
product_builder.add_node("Critic", product_critic_node)
product_builder.add_node("tools", ToolNode(product_tools))

# Add Edges
product_builder.add_edge(START, "Researcher")
product_builder.add_edge("tools", "Researcher")  # Loop back

def route_researcher(state: ProductState) -> Literal["tools", "Writer"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Writer"

product_builder.add_conditional_edges("Researcher", route_researcher)
product_builder.add_edge("Writer", "Critic")

def route_product_critic(state: ProductState) -> Literal["Writer", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Writer"
        else:
            print("[Product Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

product_builder.add_conditional_edges("Critic", route_product_critic)

product_dept_graph = product_builder.compile(checkpointer=MemorySaver())
