# KickLang Commands for Meta-AI Storybook

## Overview
This document defines the KickLang commands for managing story requests, world state updates, and synthesis output in the Meta-AI Storybook system.

## Commands

### Story Request
- **Command**: `<<story_request>>`
- **Description**: Initiates a narrative generation cycle by feeding user input into the system.
- **Usage**: `<<story_request>> {user_input}`
- **Example**: `<<story_request>> "Create a fantasy adventure story with a dragon and a hero."`

### World State Update
- **Command**: `<<world_state>>`
- **Description**: Updates the world state by sharing location and concept nodes.
- **Usage**: `<<world_state>> {location_nodes, concept_nodes}`
- **Example**: `<<world_state>> {"locations": ["Forest of Elders", "Dragon's Lair"], "concepts": ["Magic", "Bravery"]}`

### Character Update
- **Command**: `<<character_update>>`
- **Description**: Propagates trait and interaction edges for characters.
- **Usage**: `<<character_update>> {character_nodes, trait_edges, interaction_edges}`
- **Example**: `<<character_update>> {"characters": ["Hero", "Dragon"], "traits": ["brave", "fierce"], "interactions": ["Hero interacts_with Dragon"]}`

### Plot Point
- **Command**: `<<plot_point>>`
- **Description**: Triggers event nodes and precedence links to advance the plot.
- **Usage**: `<<plot_point>> {event_nodes, precedence_links}`
- **Example**: `<<plot_point>> {"events": ["Hero enters Forest", "Dragon awakens"], "precedence": ["Hero enters Forest precedes Dragon awakens"]}`

### Synthesis Output
- **Command**: `<<synthesis_output>>`
- **Description**: Compiles the final narrative segment from inputs provided by Storyteller, WorldBuilder, CharacterManager, and PlotWeaver.
- **Usage**: `<<synthesis_output>> {narrative_segment}`
- **Example**: `<<synthesis_output>> "In the heart of the Forest of Elders, the Hero encountered the fierce Dragon, marking the beginning of an epic adventure."`

## Placeholder Pipes
Placeholder pipes enable inter-role communication over the knowledge graph:
- `<<story_request>>`: Feeds user input to initiate cycles.
- `<<world_state>>`: Shares location and concept nodes.
- `<<character_update>>`: Propagates trait and interaction edges.
- `<<plot_point>>`: Triggers event nodes and precedence links.
- `<<synthesis_output>>`: Compiles final narrative segment.

## Knowledge Graph Integration
Graph nodes include Characters, Locations, Events, Items, Concepts. Edges link via `has_trait`, `located_in`, `precedes`, `interacts_with`, `possesses`, enabling pattern queries for coherence and retrieval.
