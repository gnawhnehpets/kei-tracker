# Architecture Patterns

**Domain:** Ship Tracking and Monitoring
**Researched:** April 14, 2026

## Recommended Architecture

The Kei Tracker employs a microservices architecture, separating concerns into a frontend, an API service, and a data synchronization service. MongoDB serves as the persistent data store. Data flows in a largely unidirectional manner from external AIS streams to the database, and then is consumed by the frontend.

```mermaid
graph TD
    A[AIS Stream via aisstream.io] -- WebSocket --> B[data-sync service]
    B -- Inserts Data --> C[MongoDB]
    C -- Queries Data --> D[API Service (FastAPI)]
    D -- HTTP Polling (Current) --> E[Frontend (React)]
    style E fill:#f9f,stroke:#333,stroke-width:2px
    E -- User Interaction --> D

    subgraph Proposed Improvement
        D_proposed[API Service (FastAPI)] -- WebSockets/SSE (Proposed) --> E_proposed[Frontend (React)]
    end
    style E_proposed fill:#ccf,stroke:#333,stroke-width:2px

    linkStyle 4 stroke:red,stroke-width:2px,stroke-dasharray: 5 5;
    linkStyle 5 stroke:green,stroke-width:2px;

```

### Component Boundaries

| Component            | Responsibility                                      | Communicates With                  |
|----------------------|-----------------------------------------------------|------------------------------------|
| **data-sync service**| Ingests real-time AIS data from external WebSocket. | AIS Stream, MongoDB                |
| **MongoDB**          | Persists AIS messages and ship data.                | data-sync service, API Service     |
| **API Service**      | Provides RESTful endpoints for ship data retrieval. | MongoDB, Frontend                  |
| **Frontend**         | User interface for displaying maps, lists, and details. | API Service                       |

### Data Flow

1.  **AIS Data Ingestion:** The `data-sync` Python service establishes a WebSocket connection to `aisstream.io` to receive real-time AIS messages (Position Reports, Ship Static Data) for predefined bounding boxes and/or specific MMSIs.
2.  **Data Persistence:** Upon receiving AIS messages, the `data-sync` service immediately inserts them into a MongoDB collection, enriching them with metadata like `MessageType`, `MetaData`, `ship_id`, and `timestamp`.
3.  **Data Retrieval (Frontend):** The React frontend, specifically through the `useShips` hook, initiates HTTP GET requests to the FastAPI `API Service` every 30 seconds (polling).
4.  **Data Processing (API):** The `API Service` queries MongoDB using `motor` to fetch the latest positions for all ships or historical data for a specific ship. It utilizes MongoDB aggregation pipelines for efficient retrieval of the latest distinct ship data.
5.  **Data Display (Frontend):** The frontend receives the processed ship data and renders it on `MapLibre GL JS` maps, ship lists, and detail panels.

## Patterns to Follow

### Pattern 1: Microservices Architecture
**What:** Decoupling the application into smaller, independent, and loosely coupled services.
**When:** Allows for independent development, deployment, and scaling of components. Facilitates technology choices best suited for each service.
**Example:** Separate `frontend`, `api`, and `data-sync` services in different Docker containers.

### Pattern 2: Asynchronous I/O for Backend
**What:** Using `async`/`await` for I/O-bound operations to handle many concurrent connections efficiently without blocking.
**When:** Essential for high-performance web APIs (FastAPI) and long-lived connections (WebSockets in `data-sync`).
**Example:** `FastAPI` endpoints and `motor` MongoDB driver leveraging Python's `asyncio`.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Frontend Polling for Real-time Data (Current)
**What:** Repeatedly making HTTP requests from the client to the server at fixed intervals to check for new data.
**Why bad:** Inefficient (many requests for no new data), introduces latency (data isn't truly live), consumes unnecessary server resources.
**Instead:** Implement true real-time communication using WebSockets or Server-Sent Events (SSE) from the `API Service` to the `Frontend`.

## Scalability Considerations

| Concern         | At 100 users                                | At 10K users                                         | At 1M users                                                                   |
|-----------------|---------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------------------|
| **API Service** | Single instance, optimized MongoDB queries. | Multiple API instances (load balancing), connection pooling, improved indexing. | Distributed API gateways, read replicas for MongoDB, caching layers (Redis). |
| **data-sync**   | Single instance, reliable WebSocket connection. | Redundant `data-sync` instances for failover, distributed message processing. | Shard AIS data ingestion (e.g., by region), advanced error recovery, distributed stream processing. |
| **MongoDB**     | Single replica set.                         | Sharding for horizontal scaling, robust replica sets for high availability. | Geo-distributed sharding, advanced indexing, dedicated hardware for I/O-intensive operations. |
| **Real-time UI**| Direct WebSockets from API to clients.      | WebSocket gateways, Pub/Sub message broker (Redis, Kafka) between API and UI. | Global WebSocket infrastructure, highly scalable message queues, CDN for static assets. |

## Sources

- `frontend/src/api/client.ts`
- `frontend/src/hooks/useShips.ts`
- `api/main.py`
- `data-sync/main.py`
- `docker-compose.yml`
