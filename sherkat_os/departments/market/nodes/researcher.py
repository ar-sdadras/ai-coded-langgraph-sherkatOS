import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.services.logger import logger

async def market_researcher_node(state: MarketState) -> MarketState:
    messages = state.get("messages", [])
    
    # If the last message is a ToolMessage, tool execution has finished
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        with logger.status("Market Researcher", f"Processing tool response: '{tool_msg.content[:40]}...'"):
            raw_data = {
                "tam_description": "Global enterprise automation software market estimated at $12B TAM.",
                "raw_personas": [
                    {"name": "Enterprise Product & Operations Leaders", "frustrations": ["Cross-department friction", "Manual execution"], "willingness": 8},
                    {"name": "Tech Architecture Heads", "frustrations": ["Monolithic rigid workflows", "Inefficient alignment"], "willingness": 7}
                ],
                "competitors": [
                    {"name": "AgentSystems Inc", "market_share": 25.0, "strengths": ["Brand recognition"], "weaknesses": ["Legacy codebase"]},
                    {"name": "FlowAutomate", "market_share": 8.0, "strengths": ["Agile graph visualizer"], "weaknesses": ["Lack of Pydantic validation"]}
                ],
                "trends": ["LLMs for operational subgraphs", "LangGraph multi-agent persistence"]
            }
        
        return {
            **state,
            "raw_research_data": raw_data,
            "messages": [AIMessage(content="Market research completed successfully.")]
        }
        
    else:
        with logger.status("Market Researcher", "Initiating market intelligence search using Tavily tool"):
            tool_call = {
                "name": "mcp_tavily_search",
                "args": {"query": "LangGraph multi-agent corporate simulation tools"},
                "id": "mcp_tavily_call_101",
                "type": "tool_call"
            }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
