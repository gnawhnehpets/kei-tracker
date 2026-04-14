# Technology Stack

**Project:** Kei Tracker
**Researched:** April 14, 2026

## Recommended Stack

### Core Frameworks
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| React      | -       | Frontend UI   | Modern, component-based, widely used for interactive UIs. |
| FastAPI    | -       | Backend API   | High-performance, asynchronous Python web framework for API endpoints. |
| Python     | -       | Backend Logic | Used for both API and data synchronization services. |

### Database
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| MongoDB    | -       | Data Storage  | Flexible, NoSQL document database suitable for storing diverse AIS message structures. |

### Infrastructure
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Docker     | -       | Containerization | Enables consistent deployment across environments with `docker-compose`. |
| Nginx      | -       | Reverse Proxy | Serves static frontend assets and proxies API requests. |

### Supporting Libraries
| Library               | Version  | Purpose                    | When to Use |
|-----------------------|----------|----------------------------|-------------|
| `@tanstack/react-query` | -        | Data Fetching & Caching    | For managing server state in React applications, including polling for updates. |
| `maplibre-gl-js`      | -        | Map Rendering              | For interactive maps in the frontend. |
| `motor`               | 3.7.0    | Asynchronous MongoDB Driver| For non-blocking database operations in FastAPI and data-sync. |
| `websockets`          | 15.0.1   | WebSocket Client/Server    | Primarily for `data-sync` to consume AIS stream; potential for real-time frontend. |
| `python-dotenv`       | 1.0.1    | Environment Variables      | For loading configuration from `.env` files. |
| `uvicorn`             | -        | ASGI Server                | To serve FastAPI applications asynchronously. |

## Alternatives Considered

| Category         | Recommended        | Alternative          | Why Not |
|------------------|--------------------|----------------------|---------|
| Database         | MongoDB            | PostgreSQL           | MongoDB's flexible schema is well-suited for varied AIS message formats; PostgreSQL might require more upfront schema design for this use case. |
| Frontend Polling | `@tanstack/react-query` | Raw `fetch` with `setInterval` | `react-query` provides better state management, caching, and developer experience. |

## Installation

```bash
# Frontend
npm install @tanstack/react-query maplibre-gl

# API
pip install fastapi "uvicorn[standard]" motor python-dotenv pydantic

# Data Sync
pip install websockets python-dotenv motor
```

## Sources

- `frontend/package.json`
- `api/requirements.txt`
- `data-sync/requirements.txt`
- Codebase analysis (`client.ts`, `useShips.ts`, `main.py` files)
