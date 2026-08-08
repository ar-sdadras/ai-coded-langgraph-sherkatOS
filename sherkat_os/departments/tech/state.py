from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class TechState(TypedDict):
    """
    Isolated state for the Tech Department sub-graph.
    """
    prd: Dict[str, Any]
    tech_stack: Optional[Dict[str, Any]]
    tech_blueprint: Optional[Dict[str, Any]]
    critic_feedback: Optional[str]
    retry_count: int
    messages: Annotated[List[AnyMessage], add_messages]
