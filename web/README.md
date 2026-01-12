# 🖥️ MetaCognito Web Interface

The **MetaCognito Web Interface** is a modern, reactive frontend designed to interact with the MetaCognito Orchestration Engine. It provides a visual narrative experience, real-time graph exploration, and direct control over the story generation process.

Built with **React**, **Vite**, and **TailwindCSS**.

## 🌟 Features

-   **Interactive Chat**: Conversational interface for guiding the narrative.
-   **Live Graph Visualization**: See the Knowledge Graph evolve in real-time as the story progresses.
-   **Event Stream**: Monitor internal agent decisions and system events via Server-Sent Events (SSE).
-   **System Controls**: Reset, transform, and manage the story state.

## 🚀 Getting Started

### Prerequisites

-   **Node.js** (v18+ recommended)
-   **pnpm** (recommended package manager)

### 📦 Installation

Navigate to the `web` directory and install dependencies:

```bash
cd web
pnpm install
```

### 🏃 Running the Application

Start the development server:

```bash
pnpm dev
```

The application will typically be available at `http://localhost:5173`.

> **Note**: Ensure the [API Server](../src/api/README.md) is running on port 8000 for the frontend to function correctly.

## 🛠️ Configuration

The frontend connects to the backend API. Default configuration assumes the API is at `http://localhost:8000`.

To build for production:

```bash
pnpm build
```

## 📂 Structure

-   `src/components`: UI components (Graph, Chat, Controls).
-   `src/hooks`: Custom React hooks for API interaction.
-   `src/api`: API client functions.
