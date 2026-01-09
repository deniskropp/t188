import asyncio
from rich.console import Console
from rich.prompt import Prompt
from src.metacognito.core import MetaCognito
from src.shared.models import SynthesisOutput

console = Console()

async def interactive_session():
    console.print("[bold green]Welcome to MetaCognito[/bold green]")
    system = MetaCognito()
    
    while True:
        user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        with console.status("[bold blue]Thinking...[/bold blue]"):
            result = await system.process_story_request(user_input)
            
        console.print(f"[bold cyan]Storyteller[/bold cyan]: {result.narrative_segment}")
        console.print(f"[dim]Graph Nodes: {len(system.graph_store.graph.nodes)}[/dim]")
        
if __name__ == "__main__":
    asyncio.run(interactive_session())