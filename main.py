import asyncio
from sherkat_os.orchestrator.graph import orchestrator_graph
from sherkat_os.services.logger import logger
from rich.console import Console

console = Console()

async def run_simulation():
    console.print()
    console.print("[bold green]======================================================[/bold green]")
    console.print("[bold green]          SHERKATOS ENTERPRISE ORCHESTRATOR           [/bold green]")
    console.print("[bold green]          (6-DEPARTMENT CORPORATE SANDBOX)            [/bold green]")
    console.print("[bold green]======================================================[/bold green]")
    console.print()
    
    initial_state = {
        "product_idea": "An autonomous corporate simulator where agents act as department heads cooperating using LangGraph sub-graphs.",
        "market_analysis": None,
        "prd": None,
        "tech_roadmap": None,
        "financial_model": None,
        "hr_plan": None,
        "legal_compliance": None,
        "messages": []
    }
    
    config = {
        "configurable": {
            "thread_id": "sherkat_os_corporate_session_01"
        }
    }
    
    # Run Orchestrator Graph
    final_state = await orchestrator_graph.ainvoke(initial_state, config)
    
    console.print()
    console.print("[bold green]======================================================[/bold green]")
    console.print("[bold green]          SIMULATION WORKFLOW COMPLETED               [/bold green]")
    console.print("[bold green]======================================================[/bold green]")
    console.print()
    
    # Print 6 Professional Reports
    if final_state.get("market_analysis"):
        logger.log_report("1. Final Market Analysis Report", final_state["market_analysis"], "green")
        
    if final_state.get("prd"):
        logger.log_report("2. Final Product Requirement Document (PRD)", final_state["prd"], "yellow")
        
    if final_state.get("tech_roadmap"):
        logger.log_report("3. Final Technical Blueprint", final_state["tech_roadmap"], "cyan")
        
    if final_state.get("financial_model"):
        logger.log_report("4. Final Financial Model", final_state["financial_model"], "magenta")
        
    if final_state.get("hr_plan"):
        logger.log_report("5. Final HR & Operations Staffing Plan", final_state["hr_plan"], "blue")
        
    if final_state.get("legal_compliance"):
        logger.log_report("6. Final Legal & Compliance Audit", final_state["legal_compliance"], "red")

if __name__ == "__main__":
    asyncio.run(run_simulation())
