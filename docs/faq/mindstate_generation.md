# How does the planner generate a MindState?

The `MetaCognitoPlanner.plan_pipeline` orchestrates a chain of specialized roles to generate a `MindState` without writing story text:

1.  **Researcher**: Finds cues in the recent history and graph.
2.  **Analyst**: Clusters these cues into latent patterns.
3.  **Subconscious Storyteller**: Summarizes a "dream" narrative (internal only).
4.  **Subconscious Planner**: Sequences an `ImplicitPlan` (step-by-step actions).

The result is a structured `MindState` object, returned to the CLI but not appended to the story history.
