import asyncio
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from typing import Optional

from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput, MindState

app = typer.Typer(help="MetaCognito Storybook Orchestration Engine")
console = Console()

def _display_mind_state(state: MindState):
    """Formats and displays the subconscious mind state."""
    console.print(Panel(state.dream.narrative if state.dream else "No dream narrative", title="[bold magenta]Dream Narrative[/bold magenta]", border_style="magenta"))
    
    table = Table(title="Subconscious Planning Details", show_header=True, header_style="bold cyan")
    table.add_column("Category", style="dim")
    table.add_column("Details")
    
    table.add_row("Cues", "\n".join([f"• {c.cue} [dim]({c.context})[/dim]" for c in state.cues]) if state.cues else "None")
    table.add_row("Patterns", "\n".join([f"• {p.pattern} [dim](strength: {p.strength})[/dim]" for p in state.patterns]) if state.patterns else "None")
    table.add_row("Plan Steps", "\n".join([f"{i+1}. {s}" for i, s in enumerate(state.plan.steps)]) if state.plan and state.plan.steps else "None")
    
    console.print(table)

async def _process_request(system: MetaCognito, user_input: str, mind_state: Optional[MindState] = None):
    with console.status("[bold blue]Orchestrating Narrative Agents...[/bold blue]") as status:
        async def update_status(phase: str, message: str):
            status.update(f"[bold blue]{phase}[/bold blue]: {message}")
            await asyncio.sleep(0.5) # Slight delay for visual effect
            
        result = await system.process_story_request(user_input, callback=update_status, mind_state=mind_state)
    
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
            self.commands = ["/help", "/exit", "/quit", "/clear", "/reset", "/graph", "/transform", "/suggest", "/plan", "/state", "/history"]

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
        staged_plan = None
        while True:
            try:
                # Use prompt_toolkit for the actual input
                prompt_text = "You > "
                if staged_plan:
                    prompt_text = "You [Planned] > "
                    
                user_input = await session.prompt_async(
                    prompt_text,
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
                console.print("[bold cyan]Commands:[/bold cyan]")
                console.print("  /suggest   : Generate contextual story starters.")
                console.print("  /plan <q>  : Stage a subconscious plan for the next step.")
                console.print("  /state     : Show the current staged plan.")
                console.print("  /transform : Force a world state update without narrative.")
                console.print("  /graph     : View Knowledge Graph entities.")
                console.print("  /history   : Show the session history.")
                console.print("  /clear     : Wipe EVERYTHING (Graph + History).")
                console.print("  /exit      : End the session.")
                continue

            if user_input == "/state":
                if staged_plan:
                    _display_mind_state(staged_plan)
                else:
                    console.print("[dim]No subconscious plan currently staged. Use /plan to pre-generate one.[/dim]")
                continue

            if user_input == "/history":
                if not system.history:
                    console.print("[dim]No narrative history yet.[/dim]")
                else:
                    table = Table(title="Session History")
                    table.add_column("Turn", justify="right")
                    table.add_column("User Input", style="cyan")
                    table.add_column("Narrative Snippet", style="italic")
                    for i, h in enumerate(system.history, 1):
                        snippet = h["story"][:100] + "..." if len(h["story"]) > 100 else h["story"]
                        table.add_row(str(i), h["user"], snippet)
                    console.print(table)
                continue

            if user_input in ["/clear", "/reset"]:
                system.reset()
                staged_plan = None
                console.print("[bold green]Success:[/bold green] System state reset.")
                continue

            if user_input == "/graph":
                # ... same logic ...
                table = Table(title="Knowledge Graph Entities")
                table.add_column("ID", style="cyan")
                table.add_column("Type", style="magenta")
                table.add_column("Description", style="green")
                for node_id, data in system.graph_store.graph.nodes(data=True):
                    desc = data.get("description") or data.get("desc") or "N/A"
                    if len(str(desc)) > 100:
                        desc = str(desc)[:100] + "..."
                    table.add_row(str(node_id), data.get("type", "Unknown"), desc)
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

            if user_input.startswith("/plan "):
                plan_input = user_input[6:].strip()
                if plan_input:
                    with console.status("[bold magenta]Accessing Subconscious...[/bold magenta]") as status:
                        async def update_status(phase: str, message: str):
                            status.update(f"[bold magenta]{phase}[/bold magenta]: {message}")
                            await asyncio.sleep(0.5)
                        staged_plan = await system.plan(plan_input, callback=update_status)
                    _display_mind_state(staged_plan)
                    console.print("[bold cyan]Subconscious Plan Staged.[/bold cyan] Next request will utilize this intuition.")
                continue

            if user_input.startswith("/transform "):
                transform_input = user_input[11:].strip()
                if transform_input:
                    with console.status("[bold yellow]Transforming World State...[/bold yellow]") as status:
                        async def update_status(phase: str, message: str):
                            status.update(f"[bold yellow]{phase}[/bold yellow]: {message}")
                            await asyncio.sleep(0.5)
                        await system.transform_state(transform_input, callback=update_status)
                    console.print("[bold green]World State Updated.[/bold green] The Knowledge Graph has been evolved.")
                continue

            # Handle numeric suggestion selection
            if user_input.isdigit():
                idx = int(user_input) - 1
                if 0 <= idx < len(suggestions_ref["list"]):
                    user_input = suggestions_ref["list"][idx]
                    console.print(f"[bold cyan]Using suggestion:[/bold cyan] {user_input}")

            await _process_request(system, user_input, mind_state=staged_plan)
            staged_plan = None # Clear after use
            
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
    system = MetaCognito()
    system.reset()
    console.print("[bold green]Success:[/bold green] Knowledge Graph and history cleared.")

@app.command()
def graph():
    """Inspect the current Knowledge Graph state."""
    system = MetaCognito()
    table = Table(title="Knowledge Graph Entities")
    table.add_column("ID", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Description", style="yellow")
    table.add_column("Properties", style="green")

    for node_id, data in system.graph_store.graph.nodes(data=True):
        desc = data.get("description") or data.get("desc") or "N/A"
        table.add_row(str(node_id), data.get("type", "Unknown"), desc, str(data))

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

@app.command()
def plan(
    input_text: str = typer.Argument(..., help="The story request to plan for")
):
    """Run only the subconscious planning phase to see internal reasoning."""
    system = MetaCognito()
    
    async def execute():
        with console.status("[bold magenta]Accessing Subconscious...[/bold magenta]") as status:
            async def update_status(phase: str, message: str):
                status.update(f"[bold magenta]{phase}[/bold magenta]: {message}")
                await asyncio.sleep(0.5)
            state = await system.plan(input_text, callback=update_status)
        
        _display_mind_state(state)

    asyncio.run(execute())

if __name__ == "__main__":
    app()