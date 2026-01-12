# How does the SuggestionService work?

The `SuggestionService.get_suggestions` method takes the current `graph_store.get_summary()` as input.

It prompts the Large Language Model (LLM) to generate relevant next steps that are **grounded** in the actual entities and relationships of the world. By feeding the graph summary as context, the system prevents generic, hallucinated, or impossible suggestions (e.g., suggesting a character interact with an object that doesn't exist).
