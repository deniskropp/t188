# How is MindState integrated with new input?

In the `process_story_request` method, the system checks for a `mind_state` argument (passed from the CLI if a plan is staged).

- **Staged Plan Exists**: The system skips the `planner.plan_pipeline` step and uses the pre-computed `MindState` as the context for the `Storyteller`.
- **No Staged Plan**: The system runs the default planning step or proceeds without one (depending on configuration).

This ensures the "rehearsed" plan is actually enacted during the performance phase.
