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
    console.print(Panel("[bold green]Welcome to MetaCognito[/bold green]\nType 'exit' or '/help' for options.", border_style="green"))
    
    from src.shared.suggestions import SuggestionService
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.styles import Style
    import os

    system = MetaCognito()
    history_path = os.path.expanduser("~/.metacognito_history")
    session = PromptSession(history=FileHistory(history_path))

    class MetaCompleter(Completer):
        def __init__(self, system, suggestions_ref):
            self.system = system
            self.suggestions_ref = suggestions_ref
            self.commands = ["/help", "/exit", "/quit", "/clear", "/graph", "/transform", "/suggest"]

        def get_completions(self, document, complete_event):
            text = document.text_before_cursor
            if text.startswith("/"):
                for cmd in self.commands:
                    if cmd.startswith(text):
                        yield Completion(cmd, start_position=-len(text))
                return

            # Offer suggestions if the line is empty or just starting
            if not text.strip() and self.suggestions_ref["list"]:
                for idx, sugg in enumerate(self.suggestions_ref["list"], 1):
                    # Show index and a bit of the text in the completion menu
                    display_text = f"[{idx}] {sugg[:50]}..."
                    yield Completion(str(idx), start_position=0, display=display_text)
                    yield Completion(sugg, start_position=-len(text))

    suggestions_ref = {"list": []}
    completer = MetaCompleter(system, suggestions_ref)

    async def loop():
        while True:
            try:
                # Use prompt_toolkit for the actual input
                user_input = await session.prompt_async(
                    "You > ",
                    completer=completer,
                    complete_while_typing=True
                )
            except (EOFError, KeyboardInterrupt):
                break

            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "/exit", "/quit"]:
                break

            if user_input == "/help":
                console.print("[bold cyan]Commands:[/bold cyan] /clear, /graph, /transform, /exit")
                continue

            if user_input == "/clear":
                system.graph_store.clear()
                console.print("[bold green]Success:[/bold green] Knowledge Graph cleared.")
                continue

            if user_input == "/graph":
                # Reuse the logic from graph command (simplified here)
                table = Table(title="Knowledge Graph Entities")
                table.add_column("ID", style="cyan")
                table.add_column("Type", style="magenta")
                for node_id, data in system.graph_store.graph.nodes(data=True):
                    table.add_row(str(node_id), data.get("type", "Unknown"))
                console.print(table)
                continue

            if user_input == "/suggest":
                graph_summary = system.graph_store.get_summary()
                with console.status("[bold yellow]Generating story suggestions...[/bold yellow]"):
                    suggestions_ref["list"] = await SuggestionService.get_suggestions(context=graph_summary)
                
                table = Table(show_header=False, box=None)
                table.add_column("Index", style="cyan", width=4)
                table.add_column("Suggestion", style="italic")
                for i, suggestion in enumerate(suggestions_ref["list"], 1):
                    table.add_row(f"[{i}]", suggestion)
                
                console.print(Panel(table, title="[bold yellow]Inspiration (Tab for more)[/bold yellow]", border_style="yellow"))
                continue

            # Handle numeric suggestion selection
            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(suggestions_ref["list"]):
                    user_input = suggestions_ref["list"][idx]
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