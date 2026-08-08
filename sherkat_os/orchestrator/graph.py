from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from sherkat_os.core.state import LinkageState
from sherkat_os.orchestrator.nodes import (
    call_market_department,
    call_product_department,
    call_tech_department,
    call_finance_department,
    call_hr_department,
    call_legal_department
)

orchestrator_builder = StateGraph(LinkageState)

# Add all 6 nodes
orchestrator_builder.add_node("MarketDept", call_market_department)
orchestrator_builder.add_node("ProductDept", call_product_department)
orchestrator_builder.add_node("TechDept", call_tech_department)
orchestrator_builder.add_node("FinanceDept", call_finance_department)
orchestrator_builder.add_node("HRDept", call_hr_department)
orchestrator_builder.add_node("LegalDept", call_legal_department)

# Define sequential flow
orchestrator_builder.add_edge(START, "MarketDept")
orchestrator_builder.add_edge("MarketDept", "ProductDept")
orchestrator_builder.add_edge("ProductDept", "TechDept")
orchestrator_builder.add_edge("TechDept", "FinanceDept")
orchestrator_builder.add_edge("FinanceDept", "HRDept")
orchestrator_builder.add_edge("HRDept", "LegalDept")
orchestrator_builder.add_edge("LegalDept", END)

# Compile with checkpointer for persistence
orchestrator_graph = orchestrator_builder.compile(checkpointer=MemorySaver())
