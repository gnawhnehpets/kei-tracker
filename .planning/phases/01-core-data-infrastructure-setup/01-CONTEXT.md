<!-- generated-by: gsd-discuss-phase -->

# Phase 1: Core Data & Infrastructure Setup - Context

**Decisions made during discussion for Phase 1.** These decisions will guide subsequent research and planning for this phase.

## 1. MongoDB Authentication Method

**Decision:** MongoDB connection credentials for the `data-sync` service will be managed using separate environment variables (`MONGO_USERNAME`, `MONGO_PASSWORD`) rather than embedding them directly in the `MONGO_URI`.

**Rationale:** This approach enhances clarity, flexibility, and security management by separating sensitive credentials from the connection string itself. It aligns with best practices for handling secrets.

## 2. Scope of AIS Pydantic Models

**Decision:** The initial Pydantic models in `data-sync/src/models/ais.py` will focus on modeling only the explicitly required AIS message types: `Message3` (position report) and `Message5` (static and voyage data). Additional message types will be incorporated as new requirements emerge in future phases.

**Rationale:** This iterative approach reduces initial complexity, accelerates development for core functionality, and prevents over-engineering for potentially unused message types.

## 3. AISStream.io API Key Usage

**Decision:** No changes are required regarding the `AISSTREAM_API_KEY` inclusion for connecting to `wss://stream.aisstream.io/v0/stream`. The current method of handling (or lack thereof) is considered sufficient and working.

**Rationale:** The existing implementation or implicit handling is deemed functional, removing the need for immediate changes or further investigation.

## 4. Handling of Unknown AIS Message Types in Parser

**Decision:** When `data-sync/src/ais/parser.py` encounters an AIS message type that does not have a defined Pydantic model, it will log a warning message and gracefully skip processing that specific unknown message.

**Rationale:** This approach ensures the `data-sync` service remains resilient and continues processing known message types even if unexpected or irrelevant message formats are received. It provides visibility into skipped messages without halting the service.

## 5. Logging Configuration for `data-sync` service

**Decision:** The basic logging configuration for the `data-sync` service will output `INFO` level messages to the console. Log messages will include a timestamp and detailed message content.

**Rationale:** This provides sufficient operational visibility during development and in production environments for understanding the service's behavior, progress, and identifying potential issues without excessive verbosity.
