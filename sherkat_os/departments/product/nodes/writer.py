import json
from langchain_core.messages import AIMessage
from sherkat_os.departments.product.state import ProductState
from sherkat_os.services.logger import logger

async def product_writer_node(state: ProductState) -> ProductState:
    logger.log_node_start("Product Writer", "Drafting complete PRD document...")
    
    draft = state.get("prd_draft") or {}
    
    prd = {
        "product_vision": draft.get("vision", "Default Vision"),
        "key_features": draft.get("features", []),
        "scope_exclusions": ["Mobile application integration", "Hardware simulations"],
        "success_metrics": ["Workflow completion rate > 95%", "State synchronization latency < 200ms"],
        "mvp_release_timeline": "6 weeks from kickoff"
    }
    
    if state.get("critic_feedback"):
        logger.log_node_start("Product Writer", f"Refining PRD based on critic feedback: '{state['critic_feedback']}'")
        prd["scope_exclusions"].append("Multi-cloud clustering deployments (post-MVP)")
        prd["success_metrics"].append("Zero state sync conflicts on retry loops")
        
    msg = AIMessage(content=f"Generated final PRD: {json.dumps(prd)}")
    return {
        **state,
        "prd_final": prd,
        "messages": [msg]
    }
