from typing import TypeVar, Generic, List, Optional
from rich.console import Console

T = TypeVar('T')
console = Console()

class Pipe(Generic[T]):
    def __init__(self, name: str):
        self.name = name
        self._buffer: List[T] = []

    def push(self, item: T):
        """Pushes an item into the pipe and logs it."""
        console.print(f"[bold cyan]PIPE({self.name}) <<[/bold cyan] {str(item)[:100]}...") # Log brief content
        self._buffer.append(item)

    def pull(self) -> Optional[T]:
        """Pulls an item from the pipe."""
        if not self._buffer:
            return None
        item = self._buffer.pop(0)
        console.print(f"[bold magenta]PIPE({self.name}) >>[/bold magenta] Delivered payload.")
        return item

    def peek(self) -> Optional[T]:
        """Peeks at the next item without removing it."""
        return self._buffer[0] if self._buffer else None

    @property
    def is_empty(self) -> bool:
        return len(self._buffer) == 0
