# What conflict resolution mechanisms are employed?

A **`ConflictResolver`** class (`src/metacognito/resolver.py`) compares the outputs of the parallel agents (Plot vs. World vs. Characters).

- **Directives**: If a conflict is detected (e.g., intense action in the plot contradicting character traits), the resolver issues a directive (e.g., "Ensure character consistency").
- **Storyteller Guidance**: This directive is passed to the `Storyteller` to guide valid generation.
- **Critic Loop**: A `Critic` service also reviews the final generated narrative against the graph state, triggering a refinement loop if the output is inconsistent.
