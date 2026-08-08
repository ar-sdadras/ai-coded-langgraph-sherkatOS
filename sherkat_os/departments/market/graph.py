from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from sherkat_os.departments.market.state import MarketState
from sherkat_os.departments.market.nodes.researcher import market_researcher_node
from sherkat_os.departments.market.nodes.analyst import market_analyst_node
from sherkat_os.departments.market.nodes.critic import market_critic_node
from sherkat_os.departments.market.tools import market_tools
from sherkat_os.config.settings import settings

market_builder = StateGraph(MarketState)

# Add Nodes
market_builder.add_node("Researcher", market_researcher_node)
market_builder.add_node("Analyst", market_analyst_node)
market_builder.add_node("Critic", market_critic_node)
market_builder.add_node("tools", ToolNode(market_tools))

# Add Edges
market_builder.add_edge(START, "Researcher")
market_builder.add_edge("tools", "Researcher")  # Loop back after tool execution

def route_researcher(state: MarketState) -> Literal["tools", "Analyst"]:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    return "Analyst"

market_builder.add_conditional_edges("Researcher", route_researcher)
market_builder.add_edge("Analyst", "Critic")

def route_market_critic(state: MarketState) -> Literal["Analyst", "__end__"]:
    max_retries = settings.max_retries
    if state.get("critic_feedback") is not None:
        if state.get("retry_count", 0) < max_retries:
            return "Analyst"
        else:
            print("[Market Dept Guardrail] Max retries reached, forcing exit.")
    return "__end__"

market_builder.add_conditional_edges("Critic", route_market_critic)

market_dept_graph = market_builder.compile(checkpointer=MemorySaver())
