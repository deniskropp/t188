from src.shared.models import StoryRequest, PlotPoint

class PlotWeaverService:
    async def weave_plot(self, request: StoryRequest) -> PlotPoint:
        # Mock logic to extract plot elements
        return PlotPoint(
            events=[f"Action triggered by '{request.user_input[:20]}...'", "Consequence unfolds"],
            precedence=["Action precedes Consequence"]
        )
