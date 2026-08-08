from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class LegalState(TypedDict):
    """
    Isolated state for the Legal/Compliance Department sub-graph.
    """
    prd: Dict[str, Any]
    tech_roadmap: Dict[str, Any]
    market_analysis: Dict[str, Any]
    legal_draft: Optional[Dict[str, Any]]
    legal_compliance: Optional[Dict[str, Any]]
    critic_feedback: Optional[str]
    retry_count: int
    messages: Annotated[List[AnyMessage], add_messages]
