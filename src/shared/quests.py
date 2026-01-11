import time
from typing import List, Optional, Dict, Any
from src.shared.models import Quest, Badge, LoopStatus

class QuestOrchestrator:
    def __init__(self):
        self.quests: Dict[str, Quest] = {
            "q1": Quest(
                id="q1",
                title="Exploration",
                description="Discover 5 new entities in the canvas.",
                requirements={"node_count": 5},
                reward_badge_id="b1"
            ),
            "q2": Quest(
                id="q2",
                title="Conflict",
                description="Negotiate with the canvas resistance 3 times.",
                requirements={"negotiations": 3},
                reward_badge_id="b2"
            ),
            "q3": Quest(
                id="q3",
                title="Resolution",
                description="Paint a shared future for an entity.",
                requirements={"future_painted": True},
                reward_badge_id="b3"
            )
        }
        self.badges: Dict[str, Badge] = {
            "b1": Badge(id="b1", name="First Alliance", description="You have bonded with the basic structures of the canvas.", icon="sparkles", earned_at=0),
            "b2": Badge(id="b2", name="Painter of Chaos", description="You mastered the canvas's resistance.", icon="shield", earned_at=0),
            "b3": Badge(id="b3", name="Ethical Creator", description="Your vision and the canvas's growth are one.", icon="heart", earned_at=0)
        }
        self.earned_badge_ids: List[str] = []
        self.recent_pipes: List[str] = []

    def pulse_pipe(self, message: str):
        """Adds a new semantic signal to the recent pipes queue."""
        self.recent_pipes.append(message)
        if len(self.recent_pipes) > 3:
            self.recent_pipes.pop(0)

    def update_quest_progress(self, quest_id: str, progress: float):
        if quest_id in self.quests:
            self.quests[quest_id].progress = min(progress, 1.0)
            if self.quests[quest_id].progress >= 1.0:
                self.quests[quest_id].status = "completed"

    def claim_badge(self, quest_id: str) -> Optional[Badge]:
        quest = self.quests.get(quest_id)
        if quest and quest.status == "completed" and quest.reward_badge_id:
            badge = self.badges.get(quest.reward_badge_id)
            if badge and badge.id not in self.earned_badge_ids:
                badge.earned_at = time.time()
                self.earned_badge_ids.append(badge.id)
                quest.status = "claimed"
                return badge
        return None

    def get_loop_status(self, dopamine: float, flow: float, engagement: float = 0.0) -> LoopStatus:
        return LoopStatus(
            dopamine_density=dopamine,
            flow_time=flow,
            oxytocin_level=0.5,
            engagement_index=engagement,
            active_quests=list(self.quests.values()),
            earned_badges=[self.badges[bid] for bid in self.earned_badge_ids],
            last_action_at=time.time(),
            current_pipes=self.recent_pipes or ["Idle: Waiting for input..."]
        )
