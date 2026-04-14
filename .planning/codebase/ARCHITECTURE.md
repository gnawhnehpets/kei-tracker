# Architecture

**Analysis Date:** 2026-04-14

## Pattern Overview

**Overall:** Microservices Architecture (Frontend, API, Data Sync) with a React SPA for the frontend.

**Key Characteristics:**
- **Decoupled Services:** Frontend, API, and Data Sync are separate, independently deployable units.
- **Client-Side Routing:** Frontend handles routing with React Router DOM.
- **Data Fetching/Caching:** React Query manages server state in the frontend.

## Layers

**Frontend:**
- Purpose: User interface and interaction.
- Location: `frontend/`
- Contains: React components, pages, hooks, API client.
- Depends on: API service for data.
- Used by: End-users via web browser.

**API Service:**
- Purpose: Provide data to the frontend and other services.
- Location: `api/`
- Contains: Python application logic, likely data retrieval/manipulation endpoints.
- Depends on: Data storage (assumed, needs further investigation), Data Sync service.
- Used by: Frontend service.

**Data Sync Service:**
- Purpose: Ingest and process data.
- Location: `data-sync/`
- Contains: Python application logic, likely data processing and persistence.
- Depends on: External data sources (assumed, needs further investigation), data storage (assumed).
- Used by: N/A (likely a background service).

## Data Flow

**Frontend Data Fetching:**

1.  **User Interaction:** User navigates or triggers data refresh in the `frontend`.
2.  **React Query Hook:** A React Query hook (e.g., `useShips`, `useShipHistory`) calls the `frontend/src/api/client.ts`.
3.  **API Client:** `frontend/src/api/client.ts` makes an HTTP request to the **API Service**.
4.  **API Service Processing:** The **API Service** processes the request, retrieves data (e.g., from a database), and returns it.
5.  **Data to Frontend:** The frontend receives the data, React Query caches it, and the UI updates.

**State Management:**
- **Client-side State:** Managed by React components using `useState`, `useRef`, etc.
- **Server-side State:** Managed and cached by `@tanstack/react-query` for data fetched from the API.
- **Routing State:** Managed by `react-router-dom`.

## Key Abstractions

**React Components:**
- Purpose: Reusable UI elements.
- Examples: `frontend/src/components/ShipMarker.tsx`, `frontend/src/components/Map.tsx`
- Pattern: Functional components with hooks.

**React Hooks:**
- Purpose: Encapsulate reusable logic, often for data fetching.
- Examples: `frontend/src/hooks/useShipHistory.ts`, `frontend/src/hooks/useShips.ts`
- Pattern: Custom hooks returning data and loading/error states.

**API Client Functions:**
- Purpose: Standardized interface for interacting with the backend API.
- Examples: `frontend/src/api/client.ts` (functions like `fetchShipHistory`, `fetchShips`)
- Pattern: Asynchronous functions making HTTP requests.

## Entry Points

**Frontend Application:**
- Location: `frontend/src/main.tsx`
- Triggers: Browser loading `index.html` which loads `main.tsx`.
- Responsibilities: Initialize React app, setup routing, provide global query client.

**API Service:**
- Location: `api/main.py`
- Triggers: Execution of the Python script (e.g., via `uvicorn` or `gunicorn` in a production environment).
- Responsibilities: Handle incoming HTTP requests, process business logic, interact with data sources.

**Data Sync Service:**
- Location: `data-sync/main.py`
- Triggers: Execution of the Python script (e.g., scheduled job, daemon, or message queue listener).
- Responsibilities: Fetch data from external sources, transform it, and persist it.

## Error Handling

**Strategy:** Not explicitly detailed in current exploration.
**Frontend (Implicit):** React Query provides error states for queries. Components likely handle these.
**Backend (Assumed):** Python services would typically use try-except blocks and return appropriate HTTP status codes.

## Cross-Cutting Concerns

**Logging:** Not explicitly detected.
**Validation:** Not explicitly detected.
**Authentication:** Not explicitly detected.

---

*Architecture analysis: 2026-04-14*