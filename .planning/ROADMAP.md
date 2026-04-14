## Phases

- [ ] **Phase 1: Core Data & Infrastructure Setup** - Establish foundational data ingestion, processing, and storage.
- [ ] **Phase 2: Real-time Backend & Data Broadcast** - Implement backend services for real-time data processing and broadcasting.
- [ ] **Phase 3: Real-time Frontend Display & Live Map** - Develop core frontend components for real-time ship display on a live map with modern UI.
- [ ] **Phase 4: Ship List, Details & Basic Filtering** - Implement ship list view, detail panel, and basic filtering.
- [ ] **Phase 5: Advanced Historical Tracking & Regional Filtering** - Enable historical ship tracking and regional filtering.
- [ ] **Phase 6: System Hardening & Optimization** - Ensure system meets all performance, scalability, and availability requirements.

## Phase Details

### Phase 1: Core Data & Infrastructure Setup
**Goal**: Establish the foundational data ingestion, processing, and storage mechanisms.
**Depends on**: Nothing
**Requirements**: REQ-RT-004, REQ-RT-005, REQ-DB-001, REQ-DB-002, REQ-NF-009
**Success Criteria** (what must be TRUE):
  1. The `data-sync` service successfully ingests raw AIS messages from `aisstream.io`.
  2. The `data-sync` service processes raw AIS messages and extracts relevant ship information.
  3. Real-time and historical ship data is successfully stored in MongoDB.
  4. The database schema accommodates various AIS message types and their attributes.
  5. The database is secured against unauthorized access.
**Plans**: TBD

### Phase 2: Real-time Backend & Data Broadcast
**Goal**: Implement the backend services for real-time data processing and broadcasting to the frontend.
**Depends on**: Phase 1
**Requirements**: REQ-RT-006, REQ-DB-003, REQ-DB-005, REQ-DB-006, REQ-NF-003, REQ-NF-005, REQ-NF-006
**Success Criteria** (what must be TRUE):
  1. The backend API efficiently broadcasts real-time updates to connected frontend clients.
  2. The database is optimized for quick retrieval of the latest ship positions.
  3. Data consistency is ensured across all services interacting with the database.
  4. The system gracefully handles data ingestion failures without compromising integrity.
  5. The `data-sync` service processes incoming AIS messages with minimal delay.
  6. The system architecture supports horizontal scaling of individual services.
  7. The `data-sync` service has retry mechanisms for external data source interruptions.
**Plans**: TBD

### Phase 3: Real-time Frontend Display & Live Map
**Goal**: Develop the core frontend components to display real-time ship positions on a live map with a modern UI.
**Depends on**: Phase 2
**Requirements**: REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-FM-001, REQ-FM-002, REQ-FM-003, REQ-UI-001, REQ-UI-002, REQ-UI-003, REQ-UI-004, REQ-UI-005, REQ-NF-001, REQ-NF-008
**Success Criteria** (what must be TRUE):
  1. Ship positions on the live map update in real-time, eliminating polling.
  2. Changes in ship status are displayed as they occur on the frontend.
  3. The frontend utilizes a persistent connection (WebSockets/SSE) for updates.
  4. The map interface displays current positions of all tracked ships.
  5. Users can pan, zoom, and interact with the live map.
  6. Each ship on the map is represented by an icon, optionally indicating type or status.
  7. The user interface adheres to a modern, minimalist, clean, and intuitive aesthetic.
  8. The user interface is responsive across different screen sizes.
  9. Key actions and information are easily discoverable, and feedback is provided for user interactions.
  10. Real-time ship position updates display with a latency of less than 2 seconds.
  11. All data in transit between services and to the frontend is encrypted.
**Plans**: TBD
**UI hint**: yes

### Phase 4: Ship List, Details & Basic Filtering
**Goal**: Implement the ship list view, detail panel, and basic filtering capabilities for a comprehensive user experience.
**Depends on**: Phase 3
**Requirements**: REQ-FM-004, REQ-FM-005, REQ-FM-006, REQ-FM-007, REQ-FM-008, REQ-FM-013
**Success Criteria** (what must be TRUE):
  1. A list view of all tracked ships is provided, displaying essential information.
  2. Users can select a ship from the list to view its details.
  3. The ship list is sortable and searchable by relevant attributes.
  4. Upon selecting a ship, a panel displays detailed information about that ship.
  5. The details panel includes dynamically updating real-time data for the selected ship.
  6. Users can filter ships by type (e.g., cargo, passenger, tanker).
**Plans**: TBD
**UI hint**: yes

### Phase 5: Advanced Historical Tracking & Regional Filtering
**Goal**: Enable users to view historical ship tracks and filter by geographical regions.
**Depends on**: Phase 4
**Requirements**: REQ-DB-004, REQ-FM-009, REQ-FM-010, REQ-FM-011, REQ-FM-012, REQ-NF-002
**Success Criteria** (what must be TRUE):
  1. The database supports efficient querying of historical ship movements for a given time range and ship.
  2. Users can view the historical track of a selected ship over a specified time period.
  3. The historical track is displayed as a path on the map.
  4. Users can specify custom date and time ranges for historical data retrieval.
  5. Users can filter ships displayed on the map and in the list by specific geographical regions.
  6. The API responds to data queries within 500ms under normal load.
**Plans**: TBD
**UI hint**: yes

### Phase 6: System Hardening & Optimization
**Goal**: Ensure the system meets all performance, scalability, and availability non-functional requirements.
**Depends on**: Phase 5
**Requirements**: REQ-NF-004, REQ-NF-007
**Success Criteria** (what must be TRUE):
  1. The system is capable of tracking at least 10,000 concurrent ships without significant performance degradation.
  2. The system has an uptime of 99.9% for core services.
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Data & Infrastructure Setup | 0/0 | Not started | - |
| 2. Real-time Backend & Data Broadcast | 0/0 | Not started | - |
| 3. Real-time Frontend Display & Live Map | 0/0 | Not started | - |
| 4. Ship List, Details & Basic Filtering | 0/0 | Not started | - |
| 5. Advanced Historical Tracking & Regional Filtering | 0/0 | Not started | - |
| 6. System Hardening & Optimization | 0/0 | Not started | - |
