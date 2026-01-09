import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from src.metacognito.core import MetaCognito

console = Console()

async def main():
    console.print(Panel.fit("[bold magenta]Meta-AI Storybook System[/bold magenta]\n[dim]v1.0.0 - KickLang Protocol Active[/dim]", border_style="magenta"))
    
    system = MetaCognito()
    
    console.print("[green]System initialized. Ready for story requests.[/green]")
    console.print("[dim]Type 'exit' or 'quit' to terminate session.[/dim]\n")
    
    while True:
        try:
            # Using rich's Prompt for input
            user_input = Prompt.ask("[bold cyan]story_request >>[/bold cyan]")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Shutting down MetaCognito core...[/yellow]")
                break
            
            if not user_input.strip():
                continue
                
            with console.status("[bold green]Processing KickLang pipes...[/bold green]", spinner="dots"):
                # Simulating processing delay for effect
                await asyncio.sleep(0.5) 
                result = await system.process_story_request(user_input)
            
            console.print(Panel(result.narrative_segment, title="[bold white]Synthesis Output[/bold white]", border_style="cyan"))
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[red]Interrupted by user.[/red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass