# External Integrations

**Analysis Date:** 2026-04-14

## APIs & External Services

**Mapping:**
- MapLibre GL - Frontend mapping library. Assumed to consume map tiles, but specific service not identified.
  - SDK/Client: `maplibre-gl`
  - Auth: Not explicitly detected, likely public tile services or configured via client-side code.

## Data Storage

**Databases:**
- MongoDB (implied by `motor` usage)
  - Connection: `MONGO_URI` or similar (inferred from `python-dotenv` and `motor`)
  - Client: `motor` (asynchronous Python driver)

**File Storage:**
- Local filesystem only (not detected)

**Caching:**
- None (not detected)

## Authentication & Identity

**Auth Provider:**
- Custom (not explicitly detected)
  - Implementation: Likely handled within the FastAPI backend.

## Monitoring & Observability

**Error Tracking:**
- None (not detected)

**Logs:**
- Console logging (inferred, no dedicated logging framework detected).

## CI/CD & Deployment

**Hosting:**
- Not explicitly defined.

**CI Pipeline:**
- None (not detected)

## Environment Configuration

**Required env vars:**
- `MONGO_URI` (inferred for MongoDB connection)
- Other application-specific variables (inferred from `.env` presence)

**Secrets location:**
- `.env` file for local development.
- Production secrets location not defined.

## Webhooks & Callbacks

**Incoming:**
- None (not detected)

**Outgoing:**
- None (not detected)

---

*Integration audit: 2026-04-14*