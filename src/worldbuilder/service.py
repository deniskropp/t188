from src.shared.models import StoryRequest, WorldState

class WorldBuilderService:
    async def update_world(self, request: StoryRequest) -> WorldState:
        # Mock logic to extract world elements
        location_suffix = request.user_input.split()[-1] if request.user_input else "Unknown"
        return WorldState(
            locations=[f"Forest of {location_suffix}", "Dragon's Lair"],
            concepts=["Magic", "Bravery"]
        )
