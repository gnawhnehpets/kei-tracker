# AIS Multi-Station Coverage Plan

## Background

`main_pyais.py` currently pulls from a single raw NMEA TCP feed:

```
153.44.253.27:5631  — Kystverket (Norwegian Coastal Administration)
```

This is a **terrestrial AIS shore station** that broadcasts NMEA 0183 sentences
with NMEA 4.10 tag blocks over a public, unauthenticated TCP connection. It only
covers Norwegian and nearby North Sea waters.

The goal here is to replicate this pattern for **US coastline coverage** and
eventually build a multi-source aggregator.

---

## The Problem: There Is No USCG Equivalent

The closest US equivalent — the **USCG NAIS (National AIS System)** — does not
expose a public raw TCP stream. Access routes:

| Source | Live Stream | Format | Cost |
|---|---|---|---|
| USCG NAIS | No (historical only) | CSV download | Free |
| NOAA MarineCadastre | No (historical only) | ZIP/CSV | Free |
| aisstream.io | Yes (WebSocket) | JSON | Free (API key) |
| Marinesia | No (REST poll) | JSON | Free tier |
| AISHub | Yes (TCP or REST) | NMEA / JSON | Free w/ contribution |

---

## Path to US TCP Coverage: AISHub

**AISHub** (`aishub.net`) is the closest analog to Kystverket's open TCP feed.
It aggregates hundreds of volunteer shore stations globally, including dense US
coastline coverage.

### How to Get Access

AISHub is **contributor-based**: free access in exchange for operating and
sharing a real AIS receiver feed. Two options:

#### Option A — Contribute a Feed (Recommended)
1. Set up an AIS receiver (RTL-SDR + antenna, ~$30–50)
2. Configure `gpsd` or `rtl-ais` → pipe NMEA sentences to AISHub's assigned UDP port
3. Apply at `aishub.net/join-us` — they assign a UDP ingest port via email
4. Once approved and feed is live, receive an API key + TCP stream credentials
5. TCP endpoint format (after auth): `data.aishub.net` with credentials

**Quality requirements to maintain access:**
- ≥10 vessels average over 7 days
- ≥90% uptime
- ≤60s downsampling
- ≤10s message delay

#### Option B — AISHub REST API (No Receiver Required)
After joining, API access at `data.aishub.net/ws.php?username=...`:
- Filter by bounding box or MMSI list
- Returns JSON/XML/CSV
- **Rate limit: 1 request/minute** — coarser than TCP but still viable for polling

---

## Known Open Raw TCP AIS Feeds

These feeds are publicly accessible without authentication, same format as
`153.44.253.27:5631`. Test with: `nc <host> <port> | head -5`

| Station | IP / Host | Port | Coverage | Notes |
|---|---|---|---|---|
| Kystverket (Norway) | 153.44.253.27 | 5631 | Norwegian coast | Confirmed working |
| Kystverket (Norway) | 153.44.253.27 | 5632 | Norwegian coast | May be alt channel |
| Danish Maritime Authority | 5.9.3.152 | 9999 | Danish waters | Community-reported |
| HELCOM (Baltic) | Various | 9999 | Baltic Sea | Needs verification |

> **Note:** Public TCP feeds come and go — they are run by government agencies or
> volunteers with no SLA. Verify each before building dependence on it.

### Finding More Stations

- **`github.com/andmarios/aislib`** — README lists known open feeds
- **`cruisersforum.com`** — community thread "Free AIS data sources" has crowd-sourced IPs
- **Shodan** — search `port:9999 "AIVDM"` or `port:5631 "BSVDM"` finds exposed NMEA streams
- **pyais issues/discussions** — community posts known public endpoints

---

## US Coastline Coverage Strategy

Since no single open TCP feed covers the US, the plan is a **tiered approach**:

```
Tier 1 (TCP, near-realtime)     → Open station feeds as discovered
Tier 2 (WebSocket, realtime)    → aisstream.io  [already implemented: main.py]
Tier 3 (REST, polled)           → Marinesia      [already implemented: main_marinesia.py]
Tier 4 (TCP, aggregated)        → AISHub         [pending contribution/approval]
```

For full US coastal coverage, **Tier 2 (aisstream.io)** with the appropriate
bounding boxes already covers all US waters effectively. The TCP station work
is additive — it provides redundancy and potentially different vessel populations
(e.g. smaller vessels not on satellite AIS).

---

## Proposed US Bounding Box Regions

To cover the US coastline systematically, split into regions for filtering:

```python
US_BOUNDING_BOXES = [
    # East Coast
    [[24.0, -82.0], [47.0, -66.0]],
    # Gulf of Mexico
    [[18.0, -97.0], [31.0, -80.0]],
    # West Coast
    [[32.0, -125.0], [49.0, -117.0]],
    # Alaska
    [[54.0, -170.0], [72.0, -130.0]],
    # Hawaii
    [[18.0, -161.0], [23.0, -154.0]],
    # Great Lakes (inland AIS vessels)
    [[41.0, -92.0], [48.0, -76.0]],
]
```

---

## Implementation Plan: `main_multi_station.py`

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   AsyncIO Event Loop                 │
│                                                      │
│  TCPStationTask(153.44.253.27:5631)  ──┐             │
│  TCPStationTask(<us_station_1>)      ──┤             │
│  TCPStationTask(<us_station_2>)      ──┼──► Dedup ──► MongoDB
│  TCPStationTask(AISHub TCP)          ──┤    Cache    
│  (fallback to aisstream.io WS)       ──┘             │
└─────────────────────────────────────────────────────┘
```

### Deduplication

Multiple stations will receive the same vessel broadcast. Before inserting to
MongoDB, check a short-lived in-memory cache:

```python
# Key: (mmsi, unix_timestamp // 30)  — 30s dedup window
# Value: True
dedup_cache: dict[tuple, bool] = {}
```

Any message with the same MMSI within the same 30s bucket is dropped as a
duplicate.

### Tasks

- [ ] Verify additional open TCP station IPs (Shodan / community research)
- [ ] Apply to AISHub with a contributed feed (RTL-SDR setup) for US coverage
- [ ] Implement `main_multi_station.py` with concurrent `asyncio.create_task` per station
- [ ] Add graceful per-station reconnect (one failing station doesn't kill others)
- [ ] Add dedup cache with TTL eviction
- [ ] Add `source_station` field to MongoDB documents for provenance tracking

---

## Quick Reference: Current Sources

| File | Source | Protocol | US Coverage |
|---|---|---|---|
| `main.py` | aisstream.io | WebSocket | Yes (full) |
| `main_marinesia.py` | Marinesia API | REST poll | Yes |
| `main_pyais.py` | Kystverket TCP | Raw NMEA TCP | No (Norway only) |
| `main_multi_station.py` | Multiple TCP | Raw NMEA TCP | Partial → growing |
