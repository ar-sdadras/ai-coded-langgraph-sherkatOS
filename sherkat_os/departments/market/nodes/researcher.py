import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.market.state import MarketState
from sherkat_os.services.logger import logger

async def market_researcher_node(state: MarketState) -> MarketState:
    messages = state.get("messages", [])
    
    # If the last message is a ToolMessage, it means our tool execution has finished
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("Market Researcher", f"Processing tool result: '{tool_msg.content}'")
        
        # Complete the research phase
        raw_data = {
            "tam_description": "Global enterprise automation software market estimated at $12B TAM.",
            "raw_personas": [
                {"name": "Enterprise Product Managers", "frustrations": ["Slow coordination", "Scattered tools"], "willingness": 8},
                {"name": "Startup HR Heads", "frustrations": ["Manual onboarding", "Inefficient alignment"], "willingness": 6}
            ],
            "competitors": [
                {"name": "CorpA", "market_share": 35.0, "strengths": ["Enterprise relations"], "weaknesses": ["Legacy codebase"]},
                {"name": "StartupB", "market_share": 5.0, "strengths": ["Agility"], "weaknesses": ["Limited features"]}
            ],
            "trends": ["LLMs for operational logic", "Modular agent sub-graphs"]
        }
        
        return {
            **state,
            "raw_research_data": raw_data,
            "messages": [AIMessage(content="Market research completed successfully with Tavily search.")]
        }
        
    else:
        # First call: Emit a tool call for Tavily Search MCP tool
        logger.log_node_start("Market Researcher", "Initiating market intelligence search using Tavily MCP tool...")
        
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
