import pytest
from src.shared.quests import QuestOrchestrator

def test_quest_progression():
    orchestrator = QuestOrchestrator()
    orchestrator.update_quest_progress("q1", 0.5)
    assert orchestrator.quests["q1"].progress == 0.5
    assert orchestrator.quests["q1"].status == "active"
    
    orchestrator.update_quest_progress("q1", 1.0)
    assert orchestrator.quests["q1"].status == "completed"

def test_badge_claiming():
    orchestrator = QuestOrchestrator()
    orchestrator.update_quest_progress("q1", 1.0)
    badge = orchestrator.claim_badge("q1")
    assert badge is not None
    assert badge.id == "b1"
    assert orchestrator.quests["q1"].status == "claimed"
    
    # Cannot claim twice
    badge2 = orchestrator.claim_badge("q1")
    assert badge2 is None
