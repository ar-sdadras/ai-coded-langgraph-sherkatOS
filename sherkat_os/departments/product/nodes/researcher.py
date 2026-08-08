import json
from langchain_core.messages import AIMessage, ToolMessage
from sherkat_os.departments.product.state import ProductState
from sherkat_os.services.logger import logger

async def product_researcher_node(state: ProductState) -> ProductState:
    messages = state.get("messages", [])
    
    # If the last message is a ToolMessage, process the project creation output
    if messages and isinstance(messages[-1], ToolMessage):
        tool_msg = messages[-1]
        logger.log_node_start("Product Researcher", f"Processing tool result: '{tool_msg.content}'")
        
        market_report = state.get("market_analysis") or {}
        
        prd_draft = {
            "vision": "A simulation sandbox where agent organizations cooperate.",
            "features": [
                {
                    "name": "Org Builder",
                    "description": "Visual designer to drag-and-drop agent nodes and sub-graphs.",
                    "priority": "High",
                    "stories": [
                        {
                            "as_a": "Product Manager",
                            "i_want_to": "design department topologies",
                            "so_that": "I can test workflows.",
                            "criteria": ["Support up to 10 nodes.", "Real-time state validation."]
                        }
                    ]
                }
            ]
        }
        
        return {
            **state,
            "prd_draft": prd_draft,
            "messages": [AIMessage(content="Product specifications drafted after StitchMCP workspace creation.")]
        }
        
    else:
        # First call: Emit a tool call to create a project in Stitch MCP
        logger.log_node_start("Product Researcher", "Calling StitchMCP tool to initialize product workspace...")
        
        tool_call = {
            "name": "mcp_stitch_create_project",
            "args": {"name": "SherkatOS_MVP"},
            "id": "mcp_stitch_proj_01",
            "type": "tool_call"
        }
        
        return {
            **state,
            "messages": [AIMessage(content="", tool_calls=[tool_call])]
        }
