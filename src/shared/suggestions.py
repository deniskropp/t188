from typing import List
from src.shared.models import SuggestionList
from src.shared.llm import get_llm_service
from src.shared.config import settings

STORY_SUGGESTIONS: List[str] = [
    "A lonely lighthouse keeper discovers a message in a bottle that was written by themselves, but dated fifty years in the future.",
    "In a world where memories can be traded like currency, a young thief accidentally steals the memories of a dying god.",
    "The crew of a deep-space salvage ship finds a massive, perfectly preserved Victorian mansion floating in the void of a nebula.",
    "A botanist on a distant planet discovers that the local flora is not just sentient, but is actually a biological supercomputer trying to communicate.",
    "The first time-traveler returns to the present, only to realize that every minor change they made has replaced all cats with miniature dragons.",
    "A detective who can see the 'ghosts' of objects' pasts is hired to solve the murder of a man whose body has completely disappeared.",
    "After a global blackout, everyone on Earth wakes up with the ability to speak one, and only one, random language that isn't their native tongue.",
    "A small town's annual harvest festival is interrupted when the giant pumpkin winner starts growing at an exponential rate, eventually swallowing the town square.",
]

class SuggestionService:
    @staticmethod
    async def get_suggestions(context: str = "") -> List[str]:
        """
        Fetches story suggestions from the LLM, potentially using the current world context. 
        Falls back to static suggestions if the API call fails or is unconfigured.
        """
        try:
            llm = get_llm_service()
            
            context_prompt = f"\nCURRENT WORLD CONTEXT:\n{context}\n" if context else ""
            
            prompt = f"""
            Generate 5 unique, creative, and engaging story starters for a multi-agent narrative system.
            {context_prompt}
            Each suggestion should be a single sentence that sets a compelling scene or hook.
            If context is provided, ensure the suggestions are relevant and evolve the existing world state (e.g., mention existing locations, characters, or unresolved plot points).
            Focus on different genres like Sci-Fi, Fantasy, Mystery, or Surrealism.
            """
            
            result = await llm.generate_structured(prompt, SuggestionList)
            if result and result.suggestions:
                return result.suggestions
        except Exception as e:
            # Silently log or handle error, returning static suggestions as fallback
            pass
            
        return STORY_SUGGESTIONS
