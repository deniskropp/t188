# How does the separation of intent/planning from execution enhance functionality?

The `MetaCognito` architecture separates these concerns into distinct methods: `plan()` for intent and `process_story_request()` for execution.

- **`/plan`** triggers the `MetaCognitoPlanner` pipeline (Researcher -> Analyst -> Storyteller -> Planner) to generate a purely internal `MindState`.
- **`process_story_request`** executes the narrative generation.

This separation allows the user (Director) to verify the AI's "subconscious" direction *before* any canonical story text is written. It prevents "hallucinated" or off-track narratives from becoming part of the permanent record by ensuring the plan is vetted first.
