# Theatrical Director's Model: MetaCognito Architecture

## Conceptual Overview

The MetaCognito architecture employs a "Theatrical Director's Model" to separate intent/planning from execution/narrative generation. This approach treats the AI not as a simple text generator, but as a stateful narrative engine with inspectable stages of reasoning.

Key components of this model include:

1.  **Rehearsal (`/plan`)**: Creating a staged mental model before writing. This makes the AI's reasoning inspectable and adjustable before commitment.
2.  **Script Check (`/state`)**: Exposing the "subconscious" cues, patterns, and plan steps the AI is working with.
3.  **Set Modification (`/transform`)**: Direct database manipulation to update the world state (Knowledge Graph) bypassing the narrative layer entirely.
4.  **Performance (Normal Input)**: The final execution where the AI performs the narrative generation based on the rehearsed plan and current state.
5.  **Grounding (`/graph`, `/suggest`)**: Verifying the world state and getting inspiration based on the actual graph.

## Command Mapping

| Concept | Command | Description |
| :--- | :--- | :--- |
| **Rehearsal** | `/plan <instruction>` | Runs the `planner` to generate a `MindState` (subconscious plan) without generating story text. |
| **Script Check** | `/state` | Displays the currently staged `MindState`, including cues, detected patterns, and planned steps. |
| **Set Modification** | `/transform <instruction>` | Updates the `GraphStore` (entities/edges) directly using the parallel agents (`WorldBuilder`, `CharacterManager`, `PlotWeaver`) without `Storyteller` narration. |
| **Performance** | `[Text Input]` | Runs the full pipeline: uses the staged `MindState` (if any) or generates one, then executes the parallel agents, conflict resolution, and `Storyteller` synthesis. |
| **Grounding** | `/graph` | Visualizes or lists the current nodes and edges in the Knowledge Graph. |
| **Inspiration** | `/suggest` | queries the `SuggestionService` for story starters based on the current graph context. |

## Workflow Example

1.  **Plan**: `You > /plan The hero enters a dark cave.`
    *   *System stages a plan involving "Cave", "Darkness", "Hero", "Entry".*
2.  **Inspect**: `You > /state`
    *   *System shows: Plan Step 1: "Describe the damp air using the 'Darkness' concept."*
3.  **Execute**: `You > Look around.`
    *   *System executes the staged plan combined with the new input, generating a narrative consistent with the "Darkness" plan.*
4.  **Adjust**: `You > /transform Add a hidden treasure chest to the cave.`
    *   *System adds "Treasure Chest" node to the graph located in "Cave".*
