# MetaCognito System

> **Meta-AI Storybook Orchestration Engine**

The **MetaCognito System** is an advanced narrative generation platform powered by a multi-agent AI architecture. It leverages a dynamic Knowledge Graph and the custom `KickLang` orchestration protocol to create coherent, conflict-driven, and lore-consistent stories.

## 📖 Overview

The system operates on the principle of distributed narrative responsibility. Instead of a single model generating text, distinct "Roles" (Agents) manage specific aspects of the story world (Plot, Characters, World), all coordinated by the `MetaCognito` supervisor.

### Core Objective
To generate continuous, evolving narratives where:
1.  **Consistency** is maintained by a graph database.
2.  **Character Arcs** are tracked and evolved logically.
3.  **Conflict** is structurally engineered, not just hallucinated.

## 🏗️ Architecture

### 1. The Knowledge Graph
The central "brain" of the story. Entities are nodes, and relationships are edges.
-   **Nodes**: `Character`, `Location`, `Event`, `Item`, `Concept`
-   **Edges**: `has_trait`, `located_in`, `precedes`, `interacts_with`, `possesses`

### 2. The Roles (Agents)
Specialized AI agents defined in `KickLang`:

| Role | Responsibility |
| :--- | :--- |
| **MetaCognito** | **Orchestrator**. Routes user requests and synchronizes inputs. |
| **Storyteller** | **Narrator**. Generates the final prose/output. |
| **WorldBuilder** | **Architect**. Manages setting, lore, and physical consistency. |
| **CharacterManager** | **Director**. Tracks traits, dialogue styles, and relationships. |
| **PlotWeaver** | **Designer**. Sequences events and drives conflict. |

### 3. Placebo Pipes (Communication)
Communication channels for inter-agent data flow:
-   `<<story_request>>`: Inbound user triggers.
-   `<<world_state>>`: Contextual data about the current scene/location.
-   `<<character_update>>`: Changes in character status or relationships.
-   `<<plot_point>>`: Structural event beats.
-   `<<synthesis_output>>`: Final assembled story segment.

## 🚀 Workflow

The generation process follows a cycle:

1.  **Input**: User sends a request via `<<story_request>>`.
2.  **Coordination**: `MetaCognito` parses the request.
3.  **Planning**: `PlotWeaver` determines the next event (`<<plot_point>>`).
4.  **Context**: `WorldBuilder` provides the setting (`<<world_state>>`) and `CharacterManager` aligns actors (`<<character_update>>`).
5.  **Synthesis**: `Storyteller` weaves these inputs into the final narrative (`<<synthesis_output>>`).

## 🛠️ Usage (Conceptual)

```bash
# Example KickLang activation
kicklang run --role MetaCognito --input "The hero enters the dark cave."
```

## 🗺️ Roadmap

See [MetaCognito Roadmap](docs/MetaCognito_Roadmap.md) for the detailed implementation plan.
