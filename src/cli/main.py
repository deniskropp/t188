import asyncio
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from typing import Optional

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput

app = typer.Typer(help="MetaCognito Storybook Orchestration Engine")
console = Console()

async def _process_request(system: MetaCognito, user_input: str):
    with console.status("[bold blue]Orchestrating Narrative Agents...[/bold blue]") as status:
        async def update_status(phase: str, message: str):
            status.update(f"[bold blue]{phase}[/bold blue]: {message}")
            await asyncio.sleep(0.5) # Slight delay for visual effect
            
        result = await system.process_story_request(user_input, callback=update_status)
    
    console.print(Panel(result.narrative_segment, title="[bold cyan]Storyteller[/bold cyan]", border_style="cyan"))
    console.print(f"[dim]Graph Nodes: {len(system.graph_store.graph.nodes)}[/dim]")

@app.command()
def interactive():
    """Start an interactive narrative session."""
    console.print(Panel("[bold green]Welcome to MetaCognito[/bold green]\nType 'exit' or 'quit' to end session.", border_style="green"))
    system = MetaCognito()
    
    async def loop():
        while True:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            await _process_request(system, user_input)
            
    asyncio.run(loop())

@app.command()
def run(
    role: str = typer.Option("MetaCognito", help="The role to execute"),
    input_text: str = typer.Argument(..., help="The story request or input")
):
    """Execute a single narrative step for a specific role."""
    system = MetaCognito()
    
    async def execute():
        if role.lower() == "metacognito":
            await _process_request(system, input_text)
        else:
            console.print(f"[bold red]Error:[/bold red] Role execution for '{role}' is currently routed through MetaCognito.")
            await _process_request(system, input_text)

    asyncio.run(execute())

@app.command()
def clear():
    """Clear the Knowledge Graph and delete the persistent storage file."""
    import os
    from src.shared.config import settings
    
    system = MetaCognito()
    system.graph_store.clear()
    
    if os.path.exists(settings.graph_storage_path):
        os.remove(settings.graph_storage_path)
        console.print(f"[bold green]Success:[/bold green] Persistent storage '{settings.graph_storage_path}' deleted.")
    
    console.print("[bold green]Success:[/bold green] Knowledge Graph cleared.")

@app.command()
def graph():
    """Inspect the current Knowledge Graph state."""
    system = MetaCognito()
    table = Table(title="Knowledge Graph Entities")
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Properties", style="green")

    for node_id, data in system.graph_store.graph.nodes(data=True):
        table.add_row(str(node_id), data.get("type", "Unknown"), str(data))

    console.print(table)

if __name__ == "__main__":
    app()