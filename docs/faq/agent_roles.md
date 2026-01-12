# What are the roles of WorldBuilder, CharacterManager, and PlotWeaver?

These agents act as specialized "set dressers" and "stage managers":

- **`WorldBuilder`**: Updates locations, items, and environment details in the `GraphStore`.
- **`CharacterManager`**: Updates character states, traits, and relationships.
- **`PlotWeaver`**: Updates plot points and tracks event timelines.

In the `/transform` process, they function purely as database updaters based on the user's intent. In the normal narrative flow, their outputs feed into the `Storyteller` for narrative synthesis.
