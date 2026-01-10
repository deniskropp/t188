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
    
    from src.shared.suggestions import SuggestionService
    
    system = MetaCognito()
    
    async def loop():
        # Load Knowledge Graph summary as context
        graph_summary = system.graph_store.get_summary()
        
        with console.status("[bold yellow]Generating story suggestions based on context...[/bold yellow]"):
            suggestions = await SuggestionService.get_suggestions(context=graph_summary)
        
        # Display Suggestions
        table = Table(title="Story Suggestions", show_header=False, box=None)
        table.add_column("Index", style="cyan", width=4)
        table.add_column("Suggestion", style="italic")
        
        for i, suggestion in enumerate(suggestions, 1):
            table.add_row(f"[{i}]", suggestion)
        
        console.print(Panel(table, title="[bold yellow]Inspiration[/bold yellow]", border_style="yellow"))
        console.print("[dim]Enter a number to use a suggestion, or type your own prompt.[/dim]\n")

        while True:
            user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Handle suggestion selection
            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(suggestions):
                    user_input = suggestions[idx]
                    console.print(f"[bold cyan]Using suggestion:[/bold cyan] {user_input}")
            
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

@app.command()
def transform(
    input_text: str = typer.Argument(..., help="The narrative transformation to apply")
):
    """Apply a narrative transformation for Knowledge Graph updates only."""
    system = MetaCognito()
    
    async def execute():
        with console.status("[bold blue]Transforming Knowledge Graph...[/bold blue]") as status:
            async def update_status(phase: str, message: str):
                status.update(f"[bold blue]{phase}[/bold blue]: {message}")
                await asyncio.sleep(0.5)
                
            await system.transform_state(input_text, callback=update_status)
        
        console.print(Panel(f"Transformation applied: [italic]{input_text}[/italic]", title="[bold green]Success[/bold green]", border_style="green"))
        console.print(f"[dim]Total Graph Nodes: {len(system.graph_store.graph.nodes)}[/dim]")

    asyncio.run(execute())

if __name__ == "__main__":
    app()