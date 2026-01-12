# What are the advantages of treating the AI as a stateful narrative engine?

The system persists state via `GraphStore` (JSON) and `MindState` objects, offering several advantages:

1.  **Consistency**: The Knowledge Graph acts as an external memory, ensuring facts remain true across sessions.
2.  **Inspectability**: Intermediate stages (Cues, Patterns, Plans) are saved as graph nodes (e.g., `SubconsciousSession`, `ImplicitPlan`) and can be viewed via `/state` or `/graph`.
3.  **Resumability**: `_load_state` and `_save_state` allow the "Director" to pick up exactly where they left off, preserving both the world state and the current "train of thought".
