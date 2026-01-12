# How does the example workflow demonstrate practical application?

The workflow (Plan → Inspect → Execute → Adjust) empowers the user to act as a **Director**, controlling the *simulation* rather than just the *string*.

1.  **Plan**: User defines intent locally (`/plan`).
2.  **Inspect**: User verifies the AI's understanding (e.g., "Cave" implies "Darkness").
3.  **Execute**: AI writes the scene using that verified understanding.
4.  **Adjust**: User retroactively adds missing elements (e.g., a "Treasure Chest") via `/transform` without breaking the narrative flow.

This has been validated by `tests/integration/test_workflow_example.py`.
