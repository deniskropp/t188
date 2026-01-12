# How is the MindState inspectable before commitment?

The `MindState` object is held in memory (e.g., as `staged_plan` in the CLI) after being returned by the `/plan` command.

- **Inspection**: The user can view it using the `/state` command, which renders the cues, patterns, and plan steps.
- **Adjustment**: If satisfied, the user proceeds. If not, they can discard it or issue a new `/plan` command. The architecture supports modification by separating the plan object from the execution loop.
