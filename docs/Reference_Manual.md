# 🧠 MetaCognito Reference Manual 📖

This manual provides a detailed technical reference for the **MetaCognito Storybook Orchestration Engine**, its commands, architecture, and configuration. 🛠️✨

## 🕹️ CLI Reference 💻

MetaCognito is primarily interacted with via the CLI: `python -m src.cli.main [COMMAND]`. ⌨️

### Primary Commands 🛠️

#### `interactive` 🎮
Starts a continuous narrative session. 🕹️
- **Interactive Commands:** ⌨️
    - 💡 `/help`: Show available commands.
    - 🔍 `/suggest`: Generate 5 contextual story starters based on the current graph state.
    - 💭 `/plan <input>`: Run the subconscious planner for a prompt and **stage** it for the next story beat.
    - 📋 `/state`: View the currently staged subconscious plan.
    - 🕸️ `/graph`: Display a summary table of the Knowledge Graph.
    - 📜 `/history`: Show the conversation log of narrative segments.
    - ⚡ `/transform <input>`: Apply a graph update without generating prose.
    - 🗑️ `/clear` or ♻️ `/reset`: Wipe the Knowledge Graph and session history.
    - 🚪 `/exit` or `/quit`: Terminate the session.

#### `run [INPUT]` 🏃‍♂️
Executes a single narrative step. 🎞️
- **Options:** ⚙️
  - `--role`: Specific role to execute (default: `MetaCognito` for full orchestration).

#### `plan [INPUT]` 💭
Runs the standalone subconscious planning pipeline. 🧠 Displays the internal "Reasoning" (Cues, Patterns, Dream, Implicit Steps) without updating the world or generating prose. 🕵️‍♂️

#### `graph` 🕸️
Displays the Knowledge Graph Entities in a formatted table. 📊

#### `clear` 🗑️
Resets the system state and deletes the `knowledge_graph.json` file. ♻️

#### `transform [INPUT]` ⚡
Runs a graph-only update. 🛠️ Useful for setting up a scene or forcing a world change without generating narrative text. 🌍

---

## 🏗️ Core Architecture 🏛️

### 1. Subconscious Planning Pipeline 💭
Before narrative agents (WorldBuilder, etc.) act, the system passes through a "Subconscious" phase: 🌊
1. 🔍 **Researcher**: Identifies hidden cues and missing data from the user input.
2. 📊 **Analyst**: Groups cues into latent patterns and themes.
3. ✍️ **Subconscious Storyteller**: Synthesizes patterns into a "Dream Narrative" (the 'vibe').
4. 📝 **Subconscious Planner**: Generates sequence-driven implicit steps for the agents.

**Persistence:** 💾 Planning items are stored in the graph as `SubconsciousSession`, `SubconsciousCue`, `LatentPattern`, `DreamNarrative`, and `ImplicitPlan` nodes. 🕸️

### 2. Narrative Roles 🎭
- 🌍 **WorldBuilder**: Updates locations, items, and lore.
- 👥 **CharacterManager**: Updates character traits, status, and relationships.
- 🎞️ **PlotWeaver**: Drafts plot points and drives conflict.
- ✍️ **Storyteller**: Synthesizes all agent outputs into the final prose.

---

## ⚙️ Advanced Configuration 🛠️

All settings can be configured via environment variables prefixed with `METASYS_`. 🌍

| Setting | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| `llm_provider` 🤖 | `METASYS_LLM_PROVIDER` | `mistral`, `gemini`, or `ollama` | `mistral` |
| `mistral_model` 🦊 | `METASYS_MISTRAL_MODEL` | Model ID for Mistral AI | `devstral-medium-latest` |
| `gemini_model` ♊ | `METASYS_GEMINI_MODEL` | Model ID for Google GenAI | `gemini-2.0-flash-exp` |
| `ollama_model` 🦙 | `METASYS_OLLAMA_MODEL` | Model ID for Ollama | `NSFW_DPO_Noromaid-7b-GGUF` |
| `graph_storage_path` 💾 | `METASYS_GRAPH_STORAGE_PATH` | File path for graph persistence | `knowledge_graph.json` |

---

## 🛠️ Developer Guide 🧑‍💻

### Project Structure 📂
- 🌐 `src/api`: (Reserved for future web API).
- 💻 `src/cli`: Command-line interface logic.
- 👔 `src/metacognito`: Core orchestrator and supervisor.
- 💭 `src/planner`: Subconscious planning services.
- 📦 `src/shared`: Shared models, graph logic, and LLM services.
- 🌍 `src/worldbuilder`, 👥 `src/charactermanager`, 🎞️ `src/plotweaver`, ✍️ `src/storyteller`: Narrative agent implementations.

### Adding New Roles 🎭
To add a new role, inherit from `BaseRole` in `src.shared.base` and implement the required logic, then register it in `MetaCognito.process_story_request`. 📝
