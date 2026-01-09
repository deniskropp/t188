from src.shared.models import StoryRequest, CharacterUpdate

class CharacterManagerService:
    async def update_characters(self, request: StoryRequest) -> CharacterUpdate:
        # Mock logic to extract character elements
        # Simple heuristic: treat capitalized words as potential characters
        potential_chars = [w for w in request.user_input.split() if w[0].isupper()]
        characters = potential_chars if potential_chars else ["Hero", "Dragon"]
        
        return CharacterUpdate(
            characters=characters,
            traits=["brave", "fierce"],
            interactions=[f"{characters[0]} interacts_with {characters[-1] if len(characters) > 1 else 'Self'}"]
        )
