# What are the benefits and drawbacks of this approach?

**Benefits**:
-   **Higher Coherence**: The use of a Knowledge Graph ensures long-term consistency.
-   **Reduced Hallucinations**: Planning and Grounding steps filter out impossible actions.
-   **Finer Control**: Users can dictate pacing and detail through the planning phase.

**Drawbacks**:
-   **Cost/Latency**: More steps equal higher token costs and slower response times.
-   **Learning Curve**: Users must learn specific CLI commands (`/plan`, `/state`, `/transform`).
