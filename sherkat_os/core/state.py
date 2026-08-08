from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class LinkageState(TypedDict):
    """
    Top-level Orchestrator state mapping data flows between all 6 corporate departments:
    1. Market Department (Market Intelligence & Feasibility)
    2. Product Department (PRD & User Requirements)
    3. Tech Department (Architecture Blueprint & Tech Stack)
    4. Finance Department (Unit Economics & Financial Projections)
    5. HR Department (Org Structure & Recruitment Roadmap)
    6. Legal Department (Regulatory Audits & Compliance Framework)
    """
    product_idea: str
    market_analysis: Optional[Dict[str, Any]]
    prd: Optional[Dict[str, Any]]
    tech_roadmap: Optional[Dict[str, Any]]
    financial_model: Optional[Dict[str, Any]]
    hr_plan: Optional[Dict[str, Any]]
    legal_compliance: Optional[Dict[str, Any]]
    messages: Annotated[List[AnyMessage], add_messages]
