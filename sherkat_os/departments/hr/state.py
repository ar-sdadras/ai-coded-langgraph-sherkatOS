from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class HRState(TypedDict):
    """
    Isolated state for the HR/Operations Department sub-graph.
    """
    prd: Dict[str, Any]
    tech_roadmap: Dict[str, Any]
    financial_model: Dict[str, Any]
    hr_draft: Optional[Dict[str, Any]]
    hr_plan: Optional[Dict[str, Any]]
    critic_feedback: Optional[str]
    retry_count: int
    messages: Annotated[List[AnyMessage], add_messages]
