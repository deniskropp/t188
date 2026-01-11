import pytest
import time
from src.shared.journal import SharedJournalService

@pytest.mark.asyncio
async def test_journal_logging():
    service = SharedJournalService()
    entry = await service.log_entry("stroke", "azure tree", {"x": 10}, sentiment=0.8)
    assert entry.action_type == "stroke"
    assert entry.content == "azure tree"
    assert entry.sentiment == 0.8
    assert len(service.entries) == 1

def test_dopamine_calculation():
    service = SharedJournalService()
    # Mocking time is harder here without a clock provider, but we can simulate entries
    now = time.time()
    for i in range(5):
        service.entries.append(JournalEntry(timestamp=now - i*10, action_type="stroke", content="stroke"))
    
    density = service.calculate_dopamine_density(window_seconds=100)
    # 5 actions in 100 seconds = 3 actions/min. 3/10 = 0.3 density
    assert 0.29 < density < 0.31
