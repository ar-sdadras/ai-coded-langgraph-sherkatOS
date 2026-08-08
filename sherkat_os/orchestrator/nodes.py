from typing import Dict, Any
from langchain_core.runnables import RunnableConfig

from sherkat_os.core.state import LinkageState
from sherkat_os.services.logger import logger

# Import all 6 sub-graphs
from sherkat_os.departments.market.graph import market_dept_graph
from sherkat_os.departments.product.graph import product_dept_graph
from sherkat_os.departments.tech.graph import tech_dept_graph
from sherkat_os.departments.finance.graph import finance_dept_graph
from sherkat_os.departments.hr.graph import hr_dept_graph
from sherkat_os.departments.legal.graph import legal_dept_graph

async def call_market_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("Market Department")
    
    sub_graph_input = {
        "product_idea": state["product_idea"],
        "raw_research_data": None,
        "market_report": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await market_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "market_analysis": result.get("market_report"),
        "messages": result.get("messages", [])
    }

async def call_product_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("Product Department")
    
    sub_graph_input = {
        "market_analysis": state["market_analysis"] or {},
        "prd_draft": None,
        "prd_final": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await product_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "prd": result.get("prd_final"),
        "messages": result.get("messages", [])
    }

async def call_tech_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("Tech Department")
    
    sub_graph_input = {
        "prd": state["prd"] or {},
        "tech_stack": None,
        "tech_blueprint": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await tech_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "tech_roadmap": result.get("tech_blueprint"),
        "messages": result.get("messages", [])
    }

async def call_finance_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("Finance Department")
    
    sub_graph_input = {
        "prd": state["prd"] or {},
        "tech_roadmap": state["tech_roadmap"] or {},
        "financial_draft": None,
        "financial_model": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await finance_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "financial_model": result.get("financial_model"),
        "messages": result.get("messages", [])
    }

async def call_hr_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("HR/Operations Department")
    
    sub_graph_input = {
        "prd": state["prd"] or {},
        "tech_roadmap": state["tech_roadmap"] or {},
        "financial_model": state["financial_model"] or {},
        "hr_draft": None,
        "hr_plan": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await hr_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "hr_plan": result.get("hr_plan"),
        "messages": result.get("messages", [])
    }

async def call_legal_department(state: LinkageState, config: RunnableConfig) -> Dict[str, Any]:
    logger.log_department_start("Legal/Compliance Department")
    
    sub_graph_input = {
        "prd": state["prd"] or {},
        "tech_roadmap": state["tech_roadmap"] or {},
        "market_analysis": state["market_analysis"] or {},
        "legal_draft": None,
        "legal_compliance": None,
        "critic_feedback": None,
        "retry_count": 0,
        "messages": []
    }
    
    result = await legal_dept_graph.ainvoke(sub_graph_input, config)
    
    return {
        "legal_compliance": result.get("legal_compliance"),
        "messages": result.get("messages", [])
    }
