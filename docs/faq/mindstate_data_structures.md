# What data structures represent the MindState?

The `MindState` is a composite Pydantic model (`src/shared/models.py`) containing:

- **`cues`**: List[`SubconsciousCue`] (cue string, context string)
- **`patterns`**: List[`LatentPattern`] (pattern string, strength float)
- **`dream`**: Optional[`DreamNarrative`] (narrative string)
- **`plan`**: Optional[`ImplicitPlan`] (list of step strings)
- **`nodes`/`edges`**: Graph elements representing these mental objects for persistence in the Knowledge Graph.
