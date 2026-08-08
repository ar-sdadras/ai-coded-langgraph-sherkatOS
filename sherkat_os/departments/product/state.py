from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class ProductState(TypedDict):
    """
    Isolated state for the Product Department sub-graph.
    """
    market_analysis: Dict[str, Any]
    prd_draft: Optional[Dict[str, Any]]
    prd_final: Optional[Dict[str, Any]]
    critic_feedback: Optional[str]
    retry_count: int
    messages: Annotated[List[AnyMessage], add_messages]
