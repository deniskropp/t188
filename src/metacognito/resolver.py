from src.shared.models import PlotPoint, WorldState, CharacterUpdate
from rich.console import Console

console = Console()

class ConflictResolver:
    def resolve(self, plot: PlotPoint, world: WorldState, chars: CharacterUpdate) -> str:
        """
        Analyzes the inputs for semantic conflicts and returns a directive for the Storyteller.
        For this prototype, it detects simple keyword clashes.
        """
        directive = "No conflicts detected."
        
        # Simple heuristic: Check if Plot implies action but Char implies inaction
        plot_text = " ".join(plot.events).lower()
        char_text = " ".join(chars.interactions).lower()
        
        if "fight" in plot_text and "flee" in char_text:
            directive = "CONFLICT: Plot demands 'fight', Character wants 'flee'. FORCE EVENT: Character is cornered and must fight."
            console.print(f"[bold red]{directive}[/bold red]")
        
        return directive
