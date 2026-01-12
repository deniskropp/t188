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
        """Calculates 'dopamine density' (Dt) based on Meta-Reward optimization principles."""
        now = time.time()
        recent_entries = [e for e in self.entries if now - e.timestamp < window_seconds]
        if not recent_entries:
            return 0.0
        
        # Extrinsic: Action frequency (Competence Signal)
        # Normalize: 15 actions/min is '1.0' density for high-performance state
        actions_per_min = len(recent_entries) / (window_seconds / 60)
        r_extrinsic = min(actions_per_min / 15.0, 1.0)
        
        # Intrinsic: Sentiment and Diversity (Autonomy/Novelty Signal)
        sentiments = [e.sentiment for e in recent_entries if e.sentiment is not None]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.5
        r_intrinsic = max(0.0, avg_sentiment) # Focus on positive surprise
        
        # Meta-Reward Balance (Lambda)
        # For simplicity in this engine, we use a balanced 0.5
        lambd = 0.5
        density = (lambd * r_extrinsic) + ((1 - lambd) * r_intrinsic)
        
        return min(density, 1.0)

    def calculate_bond_level(self, window_seconds: int = 1200) -> float:
        """Calculates 'SozialeZugehörigkeit' (Bond/Oxytocin) based on interactive reciprocity."""
        now = time.time()
        recent_interactions = [e for e in self.entries if e.action_type == "interaction" and now - e.timestamp < window_seconds]
        
        # Base bond is 0.5 (neutral/established)
        # Increases with frequency of interactions (reciprocity)
        reciprocity_factor = min(len(recent_interactions) / 5.0, 0.5)
        return 0.5 + reciprocity_factor

    def calculate_flow_time(self) -> float:
        """Calculates uninterrupted session duration in seconds."""
        if not self.entries:
            return 0.0
        return time.time() - self.entries[0].timestamp

    def calculate_engagement_index(self) -> float:
        """Calculates the composite EngagementIndex = (Coherence * Resilience * DopaminDichte) / SystemDrift"""
        dopamine = self.calculate_dopamine_density()
        bond = self.calculate_bond_level()
        
        # Heuristics for prototype:
        # Coherence: proportional to bond and sentiment
        coherence = (bond + dopamine) / 2.0
        
        # Resilience: inverse of error frequency in last 10 mins
        now = time.time()
        recent_errors = [e for e in self.entries if e.action_type == "error" and now - e.timestamp < 600]
        resilience = 1.0 / (1.0 + len(recent_errors))
        
        # Drift: penalty for repetitive actions or session decay
        recent_contents = [e.content for e in self.entries[-5:]]
        content_drift = 1.0 + (len(recent_contents) - len(set(recent_contents))) * 0.2
        
        duration_mins = self.calculate_flow_time() / 60.0
        fatigue_drift = 1.0 + (duration_mins / 120.0) # Penalty after 2 hours
        
        drift = content_drift * fatigue_drift
        
        index = (coherence * resilience * dopamine) / drift
        
        # The doc mentions a healthy range. We scale for UI (0.0 to 1.0)
        return min(index * 2.0, 1.0) 
