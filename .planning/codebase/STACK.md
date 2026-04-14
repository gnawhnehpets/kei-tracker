# Technology Stack

**Analysis Date:** 2026-04-14

## Languages

**Primary:**
- TypeScript 5.5.3 - Frontend
- Python 3.x - API, Data Sync

**Secondary:**
- Not detected

## Runtime

**Environment:**
- Node.js (via Vite) - Frontend
- Python 3.x - API, Data Sync

**Package Manager:**
- npm (or yarn/pnpm) - Frontend (package.json exists, but lockfile not checked explicitly)
- pip - API, Data Sync
- Lockfile: package-lock.json (implied by npm), requirements.txt (explicit for Python)

## Frameworks

**Core:**
- React 18.3.1 - Frontend (via `frontend/package.json`)
- FastAPI - API (via `api/requirements.txt`)
- None explicitly detected for Data Sync beyond core Python libraries

**Testing:**
- Not explicitly detected, likely built into framework or simple setups.

**Build/Dev:**
- Vite 5.4.2 - Frontend (via `frontend/package.json`)
- TypeScript 5.5.3 - Frontend (transpilation)

## Key Dependencies

**Critical:**
- `@tanstack/react-query` 5.56.0 - Frontend (data fetching/state management)
- `maplibre-gl` 4.0.0 - Frontend (mapping library)
- `recharts` 2.13.0 - Frontend (charting library)
- `fastapi` - API (web framework)
- `motor` - API, Data Sync (asynchronous MongoDB driver)
- `websockets` 15.0.1 - Data Sync (websocket client/server)

**Infrastructure:**
- `uvicorn` - API (ASGI server for FastAPI)
- `python-dotenv` - API, Data Sync (environment variable management)
- `tailwindcss` 3.4.10, `postcss` 8.4.45, `autoprefixer` 10.4.20 - Frontend (CSS styling)

## Configuration

**Environment:**
- Configured via `.env` file for environment variables.
- `python-dotenv` used in API and Data Sync for loading these variables.
- Frontend likely accesses environment variables prefixed with `VITE_` via Vite's environment variable handling.

**Build:**
- `vite.config.ts` (implied by Vite usage) - Frontend
- `tsconfig.json` (implied by TypeScript usage) - Frontend

## Platform Requirements

**Development:**
- Node.js compatible environment for frontend development.
- Python 3.x compatible environment for API and Data Sync development.

**Production:**
- Not explicitly defined, but likely a Linux-based environment for both Node.js and Python applications.

---

*Stack analysis: 2026-04-14*