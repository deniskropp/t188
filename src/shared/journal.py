import time
from typing import List, Optional
from src.shared.models import JournalEntry

class SharedJournalService:
    def __init__(self):
        self.entries: List[JournalEntry] = []

    async def log_entry(self, action_type: str, content: str, metadata: dict = None, sentiment: float = None) -> JournalEntry:
        """Logs a new artistic action or reflection."""
        entry = JournalEntry(
            timestamp=time.time(),
            action_type=action_type,
            content=content,
            metadata=metadata or {},
            sentiment=sentiment
        )
        self.entries.append(entry)
        return entry

    def get_entries(self, limit: int = 50) -> List[JournalEntry]:
        """Returns the latest journal entries."""
        return self.entries[-limit:]

    def calculate_dopamine_density(self, window_seconds: int = 600) -> float:
        """Calculates 'dopamine density' based on action frequency in the last X seconds."""
        now = time.time()
        recent_actions = [e for e in self.entries if now - e.timestamp < window_seconds]
        if not recent_actions:
            return 0.0
        # Normalize: say 10 strokes/min is '1.0' density
        actions_per_minute = len(recent_actions) / (window_seconds / 60)
        return min(actions_per_minute / 10.0, 1.0)

    def calculate_flow_time(self) -> float:
        """Calculates uninterrupted session duration in seconds."""
        if not self.entries:
            return 0.0
        return time.time() - self.entries[0].timestamp

    def calculate_engagement_index(self) -> float:
        """Calculates the composite EngagementIndex = (Coherence * Resilience * Dopamine) / Drift"""
        dopamine = self.calculate_dopamine_density()
        
        # Heuristics for a prototype:
        coherence = 0.9  # Placeholder: ratio of approved vs total actions
        
        # Resilience: inverse of error frequency in last 10 mins
        now = time.time()
        recent_errors = [e for e in self.entries if e.action_type == "error" and now - e.timestamp < 600]
        resilience = 1.0 / (1.0 + len(recent_errors))
        
        # Drift: penalty for repetitive actions
        recent_contents = [e.content for e in self.entries[-5:]]
        drift = 1.0 + (len(recent_contents) - len(set(recent_contents))) * 0.2
        
        index = (coherence * resilience * dopamine) / drift
        return min(index * 10, 1.0) # Scaling for UI
