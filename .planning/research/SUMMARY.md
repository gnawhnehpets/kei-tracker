# Research Summary: Kei Tracker

**Domain:** Ship Tracking and Monitoring
**Researched:** April 14, 2026
**Overall confidence:** HIGH

## Executive Summary

The Kei Tracker project currently utilizes a multi-service architecture comprising a React-based frontend, a FastAPI backend, and a Python data synchronization service. Real-time data for ship tracking is ingested via WebSockets from `aisstream.io` by the `data-sync` service and stored in MongoDB. The frontend, however, currently implements a polling mechanism (every 30 seconds) to fetch updated ship positions from the FastAPI backend, which retrieves aggregated latest positions or historical data from MongoDB. The database management relies on MongoDB, with asynchronous operations handled by `motor`.

While the data ingestion is truly real-time, the frontend's reliance on polling introduces a delay in displaying the most current ship positions. The existing MongoDB schema is flexible and directly stores AIS messages, which works for current functionalities but could be optimized for more complex queries. The project demonstrates a clear separation of concerns with its microservices approach, but the real-time update flow to the user interface could be significantly enhanced.

## Key Findings

**Stack:** React, FastAPI, Python, MongoDB, WebSockets (for ingestion), polling (for frontend updates).
**Architecture:** Multi-service (frontend, API, data-sync) with MongoDB as the central data store.
**Critical pitfall:** Frontend polling for real-time updates introduces latency and inefficiency.

## Implications for Roadmap

Based on research, suggested phase structure:

1.  **Enhance Real-time Frontend Updates** - Upgrade the frontend from polling to a true real-time mechanism to provide immediate ship position updates.
    *   Addresses: Latency in displaying live ship data, inefficient polling.
    *   Avoids: Stale data, unnecessary API calls.

2.  **Scalability & Robustness Improvements** - Implement monitoring, improved error handling, and consider message queues for broader real-time update distribution.
    *   Addresses: Potential bottlenecks with increased users/ships, system resilience.
    *   Avoids: System failures under load, data inconsistencies.

**Phase ordering rationale:**
Enhancing the frontend's real-time capabilities is the most impactful immediate improvement for user experience, as it directly addresses the discrepancy between real-time data ingestion and delayed display. Once this core real-time functionality is established, focus can shift to broader scalability and robustness.

**Research flags for phases:**
-   Phase 1: Needs deeper research into WebSocket/SSE libraries for FastAPI and React integration.
-   Phase 2: Standard patterns for message queues and monitoring, unlikely to need extensive research beyond selection of specific tools.

## Confidence Assessment

| Area        | Confidence | Notes                                                          |
|-------------|------------|----------------------------------------------------------------|
| Stack       | HIGH       | Clearly identified technologies from `package.json`, `requirements.txt`, and code. |
| Features    | HIGH       | Functionality is evident from API endpoints and frontend usage. |
| Architecture| HIGH       | Service boundaries and data flow are clear.                    |
| Pitfalls    | HIGH       | The polling mechanism is a well-understood limitation for real-time. |

## Gaps to Address

-   Detailed performance characteristics of current MongoDB setup under load.
-   Specific external real-time frameworks (e.g., Socket.IO, WebSockets directly, SSE) for FastAPI and React integration.
