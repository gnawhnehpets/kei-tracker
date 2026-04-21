# kei-tracker

A real-time AIS (Automatic Identification System) ship tracking platform. Kei-tracker ingests live vessel position broadcasts from the open ocean, stores them in MongoDB, and serves them through a FastAPI backend to a MapLibre-powered React frontend — all containerised and self-hosted on Unraid with automatic image updates via Watchtower.

---

## What it does

- Connects to the [AISStream.io](https://aisstream.io) WebSocket feed and receives live `PositionReport` and `ShipStaticData` AIS messages for a curated set of tracked vessels.
- Persists every message to MongoDB as a time-series of position records.
- Exposes a FastAPI REST API to query current positions, list all known vessels, and retrieve historical tracks.
- Renders a dark-mode live map (MapLibre GL) with directional ship markers, a side panel with speed/course/status, and a per-vessel history page with a track polyline and SOG/COG chart.

---

## Architecture

```
AISStream WebSocket
        │
        ▼
 data-sync-aisstream      ← Python / websockets / Motor (async MongoDB driver)
        │
        ▼
    MongoDB Atlas
        │
        ▼
    api (FastAPI)          ← uvicorn, Motor, Pydantic
        │
        ▼
  frontend (React)         ← Vite, TypeScript, MapLibre GL, Recharts, TanStack Query
```

Everything runs as Docker containers orchestrated by `docker-compose-unraid.yml` on a self-hosted Unraid server. Watchtower polls Docker Hub at 04:00 daily and rolls out new images automatically.

---

## Services

| Service | Image | Purpose |
|---|---|---|
| `data-sync-aisstream` | `keitracker-2` | Streams AIS messages from AISStream.io into MongoDB |
| `data-sync` | `keitracker` | Legacy/alternate data-sync (Marinesia / pyAIS) |
| `api` | `keitracker-api` | FastAPI REST API |
| `frontend` | `keitracker-frontend` | React SPA served via nginx |
| `watchtower` | `containrrr/watchtower` | Automatic image update polling |

---

## Data model

Every AIS message is stored as a flat MongoDB document, structured as received from AISStream.io with a few added fields:

```jsonc
{
  // AIS position fields (PositionReport)
  "Latitude": 59.123,
  "Longitude": 10.456,
  "Sog": 12.3,           // Speed over ground (knots)
  "Cog": 178.5,          // Course over ground (degrees)
  "TrueHeading": 179,    // 0–359; 511 = not available
  "NavigationalStatus": 0,

  // AIS static fields (ShipStaticData)
  "Name": "VESSEL NAME",
  "CallSign": "LABC1",
  "ImoNumber": 1234567,

  // AISStream metadata (present on all message types)
  "MetaData": {
    "MMSI": 257711000,
    "ShipName": "VESSEL NAME",
    "latitude": 59.1,    // receiver station lat
    "longitude": 10.4,   // receiver station lon
    "time_utc": "2026-04-21T10:00:00Z"
  },

  // Added by data-sync-aisstream
  "MessageType": "PositionReport",  // or "ShipStaticData"
  "ship_id": 257711000,
  "timestamp": "2026-04-21T10:00:00.000Z",
  "source": "aisstream"
}
```

> **Note:** `MetaData.latitude/longitude` are the AIS **receiver station** coordinates, not the vessel. Ship position is always `Latitude`/`Longitude` at the top level.

---

## API endpoints

Base path: `/api` (proxied by nginx in production)

### `GET /ships`
Returns all known vessels with their latest position and metadata. For vessels whose `PositionReport` messages carry no name, the API falls back to the most recent `ShipStaticData` record.

```jsonc
{
  "count": 13,
  "ships": [
    {
      "mmsi": 257711000,
      "ship_name": "KEI",
      "last_seen": "2026-04-21T10:00:00Z",
      "last_latitude": 59.123,
      "last_longitude": 10.456,
      "true_heading": 179,
      "cog": 178.5
    }
  ]
}
```

### `GET /ships/{mmsi}/latest`
Most recent `PositionReport` for a vessel.

### `GET /ships/{mmsi}/history`
Time-series of records for a vessel, newest first.

| Query param | Default | Description |
|---|---|---|
| `limit` | `100` | 1–1000 records |
| `message_type` | _(all)_ | `PositionReport` or `ShipStaticData` |
| `since` | _(all time)_ | ISO 8601 timestamp — return records after this time |

### `GET /health`
Returns `{"status": "ok"}`.

---

## Frontend

Built with **React 18 + TypeScript + Vite**, styled with **Tailwind CSS**, and bundled into a static site served by nginx.

**Pages**
- `/` — Live map: MapLibre GL map with rotated directional ship markers, a sidebar listing all tracked vessels, and a detail panel showing SOG, COG, and navigational status. Auto-selects MMSI 257711000 on load and flies to its last known position.
- `/ships/:mmsi` — History view: track polyline drawn on a map, plus a dual-axis **Recharts** line chart of Speed over Ground (knots) and Course over Ground (degrees) over the selected time window (1 h / 6 h / 24 h / All).

**Key libraries**
- [`maplibre-gl`](https://maplibre.org/) — open-source WebGL map renderer
- [`@tanstack/react-query`](https://tanstack.com/query) — data fetching with 30-second auto-refresh on the live map
- [`recharts`](https://recharts.org/) — SOG/COG time-series chart
- [`react-router-dom`](https://reactrouter.com/) — client-side routing

---

## CI/CD

GitHub Actions workflow (`.github/workflows/docker-publish.yml`) triggers on every push to `main`:

1. Checks out the repo and logs in to Docker Hub.
2. Builds and pushes four images in parallel using `docker/build-push-action` with GitHub Actions cache (`type=gha`):
   - `keitracker:latest` — from `./data-sync`
   - `keitracker-2:latest` — from `./data-sync-aisstream`
   - `keitracker-api:latest` — from `./api`
   - `keitracker-frontend:latest` — from `./frontend`
3. Each image is also tagged with the commit SHA for rollback.

On the Unraid host, **Watchtower** checks for updated images at 04:00 daily and restarts containers with label `com.centurylinklabs.watchtower.enable=true`.

---

## Environment variables

All secrets are passed via a `.env` file (local) or Docker Compose environment injection (production).

| Variable | Used by | Description |
|---|---|---|
| `MONGODB_URI` | all services | MongoDB connection string |
| `DATABASE_NAME` | all services | MongoDB database name |
| `DATABASE_COLLECTION` | all services | MongoDB collection name |
| `AISSTREAM_API_KEY` | data-sync-aisstream | AISStream.io WebSocket API key |
| `MARINESIA_API_KEY` | data-sync | Marinesia API key (legacy) |
| `DOCKERHUB_USERNAME` | docker-compose-unraid | Docker Hub username for image pulls |
| `DOCKERHUB_TOKEN` | docker-compose-unraid (Watchtower) | Docker Hub token for authenticated pulls |

---

## Running locally

```bash
cp .env.example .env   # fill in your keys
docker compose up --build
```

- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

---

## Tracked vessels

The data-sync-aisstream service maintains a hardcoded list of MMSIs it follows globally, including the primary vessel MMSI `257711000`. It also samples additional MMSIs from the live stream on startup and merges them in, so the tracker naturally discovers nearby traffic.
