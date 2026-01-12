# 🔌 MetaCognito API Server

The **MetaCognito API** is the backend service that exposes the core orchestration engine to external interfaces, such as the [Web Interface](../../web/README.md). It is built with **FastAPI** and provides real-time event streaming, graph visualization data, and narrative control endpoints.

For a conceptual overview of the orchestration logic, see [The Theatrical Director's Model](../../docs/Theatrical_Director_Model.md).

## 🚀 Getting Started

### Prerequisites

Ensure you have the project dependencies installed (from the project root):

```bash
pip install -r requirements.txt
```

### 🏃 Running the Server

From the project root directory, start the server using `uvicorn`:

```bash
uvicorn src.api.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## 📚 Documentation

FastAPI automatically generates interactive documentation:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔑 Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/status` | Check system health and node counts. |
| `GET` | `/api/graph` | Retrieve the full Knowledge Graph (Nodes & Edges). |
| `POST` | `/api/chat` | Send a story input and receive a narrative segment. |
| `POST` | `/api/plan` | Run the subconscious planning phase only. |
| `GET` | `/api/events` | Subscribe to real-time system events (SSE). |
| `POST` | `/api/reset` | Reset the system state and history. |

## 🛠️ Configuration

The API reads configuration from environment variables defined in the root `.env` file. See the main [README](../../README.md#configuration) for details.
