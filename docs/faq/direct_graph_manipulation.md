# How does direct manipulation bypass the narrative layer?

The `/transform` command (via the `transform_state` method) executes the parallel agents (`WorldBuilder`, `CharacterManager`, `PlotWeaver`) but **skips** the `Storyteller` and `Critic`.

It directly computes and applies updates to the `GraphStore` (WorldState, CharacterUpdate, PlotPoint). This allows "God-mode" edits—like "Add a door here"—without requiring a narrative justification or generating a story response (e.g., "Suddenly, a door appeared").
