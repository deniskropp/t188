# 🧠 MetaCognito System 🎭

> **✨ Meta-AI Storybook Orchestration Engine ✨**

The **MetaCognito System** is an advanced narrative generation platform powered by a multi-agent AI architecture. 🤖 It leverages a dynamic Knowledge Graph and the custom `KickLang` orchestration protocol to create coherent, conflict-driven, and lore-consistent stories. 📚🌌

## 📖 Overview 🧐

The system operates on the principle of distributed narrative responsibility. 🤝 Instead of a single model generating text, distinct "Roles" (Agents) manage specific aspects of the story world (Plot, Characters, World), all coordinated by the `MetaCognito` supervisor. 👔

### 🎯 Core Objective
To generate continuous, evolving narratives where:
1.  **Consistency** ⚖️ is maintained by a graph database.
2.  **Character Arcs** 📈 are tracked and evolved logically.
3.  **Conflict** ⚔️ is structurally engineered, not just hallucinated.

## 🏗️ Architecture 🏛️

MetaCognito follows a **Subconscious → Conscious** orchestration flow: 🌊

1.  **Subconscious Phase (The Planner)** 💭:
    - 🔍 Analyzes the "hidden" intent of the user.
    - 💡 Generates **Cues**, **Latent Patterns**, and a **Dream Narrative**.
    - 📝 Produces an **Implicit Plan** that instructs the narrative agents.
2.  **Conscious Phase (Narrative Agents)** 🎭:
    - 🌍 **WorldBuilder**, 👥 **CharacterManager**, and 🎞️ **PlotWeaver** update the state in parallel based on the implicit plan.
    - ✍️ **Storyteller** synthesizes the updates into the final narrative segment.

### 🕸️ The Knowledge Graph 🧠
The central "brain" of the story. Entities are nodes, and relationships are edges.
-   **Nodes** ⚪: `Character`, `Location`, `Event`, `Item`, `Concept`, `SubconsciousSession`
-   **Edges** ➡️: `has_trait`, `located_in`, `precedes`, `interacts_with`, `possesses`, `identifies_cue`

### 2. The Roles (Agents)
Specialized AI agents defined in `KickLang`:

| Role | Responsibility |
| :--- | :--- |
| **MetaCognito** | **Orchestrator**. Routes user requests and synchronizes inputs. |
| **Storyteller** | **Narrator**. Generates the final prose/output. |
| **WorldBuilder** | **Architect**. Manages setting, lore, and physical consistency. |
| **CharacterManager** | **Director**. Tracks traits, dialogue styles, and relationships. |
| **PlotWeaver** | **Designer**. Sequences events and drives conflict. |

## ⚙️ Configuration

MetaCognito uses Pydantic-based settings that can be configured via environment variables (prefixed with `METASYS_`).

### Environment Variables
| Variable | Description | Default |
| :--- | :--- | :--- |
| `METASYS_LLM_PROVIDER` | `mistral` or `gemini` | `mistral` |
| `METASYS_MISTRAL_API_KEY` | Your Mistral AI API Key | None |
| `METASYS_GOOGLE_API_KEY` | Your Google GenAI API Key | None |
| `METASYS_GRAPH_STORAGE_PATH` | Path to persistent graph JSON | `knowledge_graph.json` |

## 🚀 Getting Started

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up Environment**:
    Create a `.env` file or export your keys:
    ```bash
    export METASYS_MISTRAL_API_KEY="your-key-here"
    ```

## 🚀 Usage

### 🎮 Interactive Mode (Recommended)
Launch a continuous narrative session with full command support.
```bash
python -m src.cli.main interactive
```
**Interactive Commands:**
- `/suggest`: Get contextual story starters.
- `/plan <input>`: Pre-calculate subconscious reasoning for a beat.
- `/state`: View your currently staged plan.
- `/graph`: Inspect the world state.

### 🧠 Standalone Planning
Inspect the "thoughts" of the system without generating text.
```bash
python -m src.cli.main plan "The protagonist finds a glowing artifact."
```

### 📈 Graph Inspection
```bash
python -m src.cli.main graph
```

### 🧹 Resetting the System
Clear the Knowledge Graph and delete persistent storage.
```bash
python -m src.cli.main clear
```

For more details, see the [Reference Manual](docs/Reference_Manual.md).

## 🎭 Illustrative Example

### 1. Initial Prompt
**User**: `The hero enters the dark cave.`

### 2. Orchestration Flow
1.  **MetaCognito** receives the request.
2.  **PlotWeaver** identifies a "Discovery" beat.
3.  **WorldBuilder** defines the cave's properties (damp, smelling of ozone).
4.  **CharacterManager** updates the hero's status (cautious, holding a torch).
5.  **ConflictResolver** ensures the torch doesn't conflict with the "dark" description.
6.  **Storyteller** generates the prose.

### 3. Resulting Narrative
> "The air grew thick with the scent of wet stone and ancient ozone as Elara stepped over the threshold. Her torch flickered, casting long, dancing shadows against the jagged walls. Somewhere in the depths, a rhythmic dripping whispered of secrets long forgotten..."

### 4. Graph Update
The Knowledge Graph now includes:
-   `Location: Dark Cave` (newly explored)
-   `Character: Elara` -> `located_in` -> `Dark Cave`

## 📜 Changelog

- **Subconscious Planning v1.1**: Integrated Researcher, Analyst, and Storyteller roles into a pre-narrative pipeline.
- **Persistence 2.0**: All planning items now persist in the Knowledge Graph with automated context summarization to prevent bloat.
- **Dynamic Suggestions**: Added `/suggest` to generate lore-consistent story starters.
- **Improved CLI**: Added command auto-completion and rich status updates.
- **Mistral AI Integration**: Switched LLM provider to Mistral AI for enhanced narrative generation and structured output.
- **Conflict Resolution**: Integrated a dedicated resolver to maintain narrative logic between agents.

## 🗺️ Roadmap

See [MetaCognito Roadmap](docs/MetaCognito_Roadmap.md) for the detailed implementation plan.
