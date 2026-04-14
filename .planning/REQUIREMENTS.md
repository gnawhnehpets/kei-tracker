<!-- generated-by: gsd-doc-writer -->
# Project Requirements: Kei Tracker

This document outlines the functional and non-functional requirements for the Kei Tracker project, focusing on enhancing real-time updates, robust database management, and a modern user interface.

## 1. Project Overview

The Kei Tracker project aims to provide users with real-time tracking and monitoring of ships. The core purpose is to fix existing bugs, add new features, and improve project documentation. The target audience is end-users who require immediate and accurate ship position data and historical analysis capabilities.

## 2. Key Features

### 2.1. Real-time Updates

The system shall provide immediate and continuous updates of ship positions and related data to the user interface.

#### 2.1.1. Real-time Frontend Display
- **REQ-RT-001:** The system shall update ship positions on the live map in real-time, eliminating the current polling mechanism.
- **REQ-RT-002:** The system shall display changes in ship status (e.g., speed, course, destination) as they occur.
- **REQ-RT-003:** The frontend shall utilize a persistent connection (e.g., WebSockets or Server-Sent Events) to receive updates from the backend.

#### 2.1.2. Data Ingestion & Processing
- **REQ-RT-004:** The `data-sync` service shall continuously ingest AIS messages from `aisstream.io`.
- **REQ-RT-005:** The `data-sync` service shall process raw AIS messages and extract relevant ship information (MMSI, latitude, longitude, speed, course, status, etc.).
- **REQ-RT-006:** The backend API shall efficiently broadcast real-time updates to connected frontend clients.

### 2.2. Database Management

The system shall efficiently store, retrieve, and manage ship tracking data.

#### 2.2.1. Data Storage
- **REQ-DB-001:** The system shall store real-time and historical ship data in MongoDB.
- **REQ-DB-002:** The database schema shall accommodate various AIS message types and their attributes.
- **REQ-DB-003:** The database shall be optimized for quick retrieval of the latest ship positions.
- **REQ-DB-004:** The database shall support efficient querying of historical ship movements for a given time range and ship.

#### 2.2.2. Data Consistency & Integrity
- **REQ-DB-005:** The system shall ensure data consistency across all services that interact with the database.
- **REQ-DB-006:** The system shall handle data ingestion failures gracefully without compromising data integrity.

## 3. Functional Requirements

### 3.1. Live Ship Map
- **REQ-FM-001:** The system shall display a map interface showing the current positions of all tracked ships.
- **REQ-FM-002:** Users shall be able to pan, zoom, and interact with the live map.
- **REQ-FM-003:** Each ship on the map shall be represented by an icon, optionally indicating its type or status.

### 3.2. Ship List View
- **REQ-FM-004:** The system shall provide a list view of all tracked ships, displaying essential information (e.g., MMSI, name, last known position time).
- **REQ-FM-005:** Users shall be able to select a ship from the list to view its details.
- **REQ-FM-006:** The ship list shall be sortable and searchable by relevant attributes (e.g., MMSI, ship name).

### 3.3. Ship Details Panel
- **REQ-FM-007:** Upon selecting a ship, a panel shall display detailed information about that ship (e.g., MMSI, IMO, call sign, destination, ETA, full historical track summary).
- **REQ-FM-008:** The panel shall include dynamically updating real-time data for the selected ship.

### 3.4. Historical Tracking
- **REQ-FM-009:** Users shall be able to view the historical track of a selected ship over a specified time period.
- **REQ-FM-010:** The historical track shall be displayed as a path on the map.
- **REQ-FM-011:** Users shall be able to specify custom date and time ranges for historical data retrieval.

### 3.5. Regional Filtering
- **REQ-FM-012:** Users shall be able to filter ships displayed on the map and in the list by specific geographical regions.

### 3.6. Ship Type Filtering
- **REQ-FM-013:** Users shall be able to filter ships by type (e.g., cargo, passenger, tanker).

## 4. Non-Functional Requirements

### 4.1. Performance
- **REQ-NF-001:** The system shall display real-time ship position updates with a latency of less than 2 seconds.
- **REQ-NF-002:** The API shall respond to data queries within 500ms under normal load.
- **REQ-NF-003:** The `data-sync` service shall process incoming AIS messages with minimal delay, ensuring up-to-date information.

### 4.2. Scalability
- **REQ-NF-004:** The system shall be capable of tracking at least 10,000 concurrent ships without significant performance degradation.
- **REQ-NF-005:** The system architecture shall support horizontal scaling of individual services (frontend, API, data-sync).

### 4.3. Reliability & Availability
- **REQ-NF-006:** The `data-sync` service shall have retry mechanisms for external data source interruptions.
- **REQ-NF-007:** The system shall have an uptime of 99.9% for core services.

### 4.4. Security
- **REQ-NF-008:** All data in transit between services and to the frontend shall be encrypted (e.g., HTTPS, WSS).
- **REQ-NF-009:** The database shall be secured against unauthorized access.

## 5. UI/UX Requirements

### 5.1. Aesthetic
- **REQ-UI-001:** The user interface shall adhere to a modern and minimalist aesthetic.
- **REQ-UI-002:** The design shall be clean, uncluttered, and intuitive for navigation.

### 5.2. Responsiveness
- **REQ-UI-003:** The user interface shall be responsive and usable across different screen sizes (desktop, tablet).

### 5.3. Usability
- **REQ-UI-004:** Key actions and information shall be easily discoverable.
- **REQ-UI-005:** Feedback shall be provided for user interactions (e.g., loading states, filter applied indicators).

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-RT-001 | Phase 3 | Pending |
| REQ-RT-002 | Phase 3 | Pending |
| REQ-RT-003 | Phase 3 | Pending |
| REQ-RT-004 | Phase 1 | Pending |
| REQ-RT-005 | Phase 1 | Pending |
| REQ-RT-006 | Phase 2 | Pending |
| REQ-DB-001 | Phase 1 | Pending |
| REQ-DB-002 | Phase 1 | Pending |
| REQ-DB-003 | Phase 2 | Pending |
| REQ-DB-004 | Phase 5 | Pending |
| REQ-DB-005 | Phase 2 | Pending |
| REQ-DB-006 | Phase 2 | Pending |
| REQ-FM-001 | Phase 3 | Pending |
| REQ-FM-002 | Phase 3 | Pending |
| REQ-FM-003 | Phase 3 | Pending |
| REQ-FM-004 | Phase 4 | Pending |
| REQ-FM-005 | Phase 4 | Pending |
| REQ-FM-006 | Phase 4 | Pending |
| REQ-FM-007 | Phase 4 | Pending |
| REQ-FM-008 | Phase 4 | Pending |
| REQ-FM-009 | Phase 5 | Pending |
| REQ-FM-010 | Phase 5 | Pending |
| REQ-FM-011 | Phase 5 | Pending |
| REQ-FM-012 | Phase 5 | Pending |
| REQ-FM-013 | Phase 4 | Pending |
| REQ-NF-001 | Phase 3 | Pending |
| REQ-NF-002 | Phase 5 | Pending |
| REQ-NF-003 | Phase 2 | Pending |
| REQ-NF-004 | Phase 6 | Pending |
| REQ-NF-005 | Phase 2 | Pending |
| REQ-NF-006 | Phase 2 | Pending |
| REQ-NF-007 | Phase 6 | Pending |
| REQ-NF-008 | Phase 3 | Pending |
| REQ-NF-009 | Phase 1 | Pending |
| REQ-UI-001 | Phase 3 | Pending |
| REQ-UI-002 | Phase 3 | Pending |
| REQ-UI-003 | Phase 3 | Pending |
| REQ-UI-004 | Phase 3 | Pending |
| REQ-UI-005 | Phase 3 | Pending |
