import asyncio
from src.shared.suggestions import SuggestionService
from rich.console import Console

async def test():
    console = Console()
    console.print("[bold yellow]Testing SuggestionService with Context...[/bold yellow]")
    
    context = "The story takes place in the Lighthouse of Solitude. Elias the keeper has found a message from his future self. There is a mysterious Disco Ball of Light in the Enchanted Forest."
    
    try:
        console.print(f"[dim]Context:[/dim]\n{context}\n")
        suggestions = await SuggestionService.get_suggestions(context=context)
        console.print(f"[bold green]Received {len(suggestions)} contextual suggestions:[/bold green]")
        for i, s in enumerate(suggestions, 1):
             console.print(f"{i}. {s}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    asyncio.run(test())
