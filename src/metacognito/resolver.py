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
        
        # Simple heuristic: Check if Plot implies action
        plot_text = " ".join(plot.events).lower()
        
        # For prototype, we check if characters are mentioned in plot in a specific way
        # or just stick to the simple plot-based check for now.
        if "fight" in plot_text:
             directive = "CONFLICT DETECTED: Intense action in plot. Ensure character consistency."
             console.print(f"[bold red]{directive}[/bold red]")
        
        return directive
