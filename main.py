import asyncio
import os
import json
from pathlib import Path
from sherkat_os.orchestrator.graph import orchestrator_graph
from sherkat_os.services.logger import logger
from sherkat_os.config.settings import settings
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def export_reports(final_state: dict, output_dir: str):
    """
    Exports all generated department reports to JSON and Markdown files in the output directory.
    """
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    
    reports = {
        "market_analysis": final_state.get("market_analysis"),
        "prd": final_state.get("prd"),
        "tech_roadmap": final_state.get("tech_roadmap"),
        "financial_model": final_state.get("financial_model"),
        "hr_plan": final_state.get("hr_plan"),
        "legal_compliance": final_state.get("legal_compliance")
    }
    
    # Export master JSON
    json_path = path / "corporate_simulation_master_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)
        
    # Export executive Markdown report
    md_path = path / "corporate_simulation_executive_summary.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# SherkatOS Corporate Simulation Executive Summary\n\n")
        f.write(f"**Product Idea**: {final_state.get('product_idea', 'N/A')}\n\n")
        f.write("---\n\n")
        
        for dept_key, title in [
            ("market_analysis", "1. Market Analysis Report"),
            ("prd", "2. Product Requirement Document (PRD)"),
            ("tech_roadmap", "3. Technical Architecture Blueprint"),
            ("financial_model", "4. Financial & Unit Economics Model"),
            ("hr_plan", "5. HR & Operational Staffing Plan"),
            ("legal_compliance", "6. Legal & Compliance Audit")
        ]:
            f.write(f"## {title}\n```json\n")
            f.write(json.dumps(reports.get(dept_key) or {}, indent=2))
            f.write("\n```\n\n")
            
    console.print(f"[bold green]✓ Exported master reports to {json_path} and {md_path}[/bold green]")

async def run_simulation(user_idea: str = None):
    console.print()
    console.print(Panel.fit(
        "[bold cyan]SHERKATOS ENTERPRISE MULTI-AGENT ORCHESTRATOR[/bold cyan]\n"
        "[white]6-Department Corporate Sandbox (LangGraph Subgraphs & Pydantic v2)[/white]",
        border_style="bold green"
    ))
    console.print()
    
    if not user_idea:
        user_idea = "An autonomous corporate simulator where agents act as department heads cooperating using LangGraph sub-graphs."
    
    initial_state = {
        "product_idea": user_idea,
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
    
    console.print(f"[bold yellow]Initiating Corporate Pipeline for Product Idea:[/bold yellow] '{user_idea}'\n")
    
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

    # Export to disk
    export_reports(final_state, settings.output_dir)

if __name__ == "__main__":
    asyncio.run(run_simulation())
