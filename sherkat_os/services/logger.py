import json
import time
from contextlib import contextmanager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any, Optional

class EnterpriseLogger:
    """
    Premium structured logging using Rich formatting with real-time spinners and status tracking for SherkatOS.
    """
    def __init__(self):
        self.console = Console()
        
    def log_department_start(self, dept_name: str):
        self.console.print()
        self.console.print(Panel(
            f"[bold white]Invoking {dept_name} Sub-Graph[/bold white]",
            subtitle="SherkatOS Orchestrator Flow",
            style="bold blue on black",
            expand=False
        ))

    def log_node_start(self, node_name: str, info: str):
        self.console.print(f"[bold cyan]>>> [{node_name} Node][/bold cyan] {info}")

    @contextmanager
    def status(self, node_name: str, action: str):
        """
        Live interactive spinner context manager for long-running LLM API calls & graph steps.
        Shows live animated spinner while waiting for LLM responses.
        """
        spinner_text = f"[bold cyan]⏳ [{node_name} Node][/bold cyan] [bold yellow]{action}...[/bold yellow]"
        start_time = time.time()
        with self.console.status(spinner_text, spinner="dots", spinner_style="bold cyan") as status_obj:
            yield status_obj
            elapsed = time.time() - start_time
            self.console.print(f"[bold green]✓ [{node_name} Node][/bold green] {action} [dim]({elapsed:.1f}s)[/dim]")

    def log_critic_rejection(self, critic_name: str, feedback: str, attempt: int, max_attempts: int):
        table = Table(title="[bold red]Node Rejection[/bold red]", show_header=False, box=None)
        table.add_row("[bold yellow]Critic:[/bold yellow]", f"[red]{critic_name}[/red]")
        table.add_row("[bold yellow]Feedback:[/bold yellow]", f"[italic white]{feedback}[/italic white]")
        table.add_row("[bold yellow]Iteration:[/bold yellow]", f"[yellow]{attempt} / {max_attempts}[/yellow]")
        
        self.console.print(Panel(
            table,
            border_style="red",
            title="Critic Review",
            title_align="left",
            expand=False
        ))

    def log_critic_approval(self, critic_name: str, msg: str = "Approved"):
        self.console.print(f"[bold green]✓ [{critic_name} Approved][/bold green] {msg}")

    def log_report(self, title: str, report_data: Any, color: str = "green"):
        if hasattr(report_data, "model_dump"):
            report_data = report_data.model_dump()
        elif not isinstance(report_data, dict):
            report_data = {"report": str(report_data)}
            
        table = Table(show_header=True, header_style=f"bold {color}", box=None)
        table.add_column("Key", style="bold cyan")
        table.add_column("Value", style="white")
        
        for k, v in report_data.items():
            if isinstance(v, list):
                val_str = "\n".join([f"* {item}" for item in v])
            elif isinstance(v, dict) or (isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict)):
                val_str = json.dumps(v, indent=2)
            else:
                val_str = str(v)
            table.add_row(k.replace("_", " ").title(), val_str)
            
        self.console.print()
        self.console.print(Panel(
            table,
            title=f"[bold {color}]{title}[/bold {color}]",
            border_style=color,
            expand=False
        ))
        self.console.print()

logger = EnterpriseLogger()
