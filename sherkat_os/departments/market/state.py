from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class MarketState(TypedDict):
    """
    Isolated state for the Market Department sub-graph.
    """
    product_idea: str
    raw_research_data: Optional[Dict[str, Any]]
    market_report: Optional[Dict[str, Any]]
    critic_feedback: Optional[str]
    retry_count: int
    messages: Annotated[List[AnyMessage], add_messages]
