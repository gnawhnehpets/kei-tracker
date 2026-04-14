# Feature Landscape

**Domain:** Ship Tracking and Monitoring
**Researched:** April 14, 2026

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature             | Why Expected                                   | Complexity | Notes                                                         |
|---------------------|------------------------------------------------|------------|---------------------------------------------------------------|
| Live Ship Map       | Core functionality for tracking ship movements.| Medium     | Displays current positions, requires regular updates.         |
| Ship List View      | Overview of all tracked ships.                 | Low        | Provides quick access and basic information.                  |
| Ship Details Panel  | Detailed information about a selected ship.    | Medium     | Shows specific metadata, possibly historical data summary.    |
| Historical Tracking | View past movements of a ship.                 | Medium     | Essential for analysis and incident review.                   |
| AIS Data Ingestion  | Continuous stream of ship data.                | High       | Backend process for collecting and storing real-time AIS messages. |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature                  | Value Proposition                                  | Complexity | Notes                                                                   |
|--------------------------|----------------------------------------------------|------------|-------------------------------------------------------------------------|
| True Real-time UI Updates| Eliminates latency, provides immediate feedback.   | High       | Enhances user experience significantly for live tracking.               |
| Regional Filtering       | Focus on specific geographical areas.              | Medium     | Useful for targeted monitoring (currently implemented in `data-sync`).  |
| Ship Type Filtering      | Filter ships by type (e.g., cargo, passenger).     | Medium     | Improves usability for specific use cases.                              |
| Speed/Course Charts      | Visualize ship behavior over time.                 | Medium     | Provides deeper insights beyond just position.                          |

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature                 | Why Avoid                                              | What to Do Instead                                      |
|------------------------------|--------------------------------------------------------|---------------------------------------------------------|
| Direct AIS Stream to Frontend| Too much raw data, complex client-side processing.     | Process and aggregate data on the backend, send summarized updates. |
| Full-text Search on Raw AIS  | Overkill for current needs, resource-intensive.        | Focus on structured queries (MMSI, ship name) and geospatial. |

## Feature Dependencies

```
AIS Data Ingestion → Historical Tracking
AIS Data Ingestion → Live Ship Map
Live Ship Map ← Ship List View (List drives selection on map)
Live Ship Map ← Ship Details Panel (Map selection populates panel)
True Real-time UI Updates → Live Ship Map (Enhances existing map)
```

## MVP Recommendation

Prioritize:
1.  **Live Ship Map** - Core visual tracking.
2.  **Ship List View** - Primary navigation and overview.
3.  **Ship Details Panel** - Essential information on selected ships.
4.  **True Real-time UI Updates** - Critical enhancement for live experience.

Defer: Ship Type Filtering, Speed/Course Charts: These add value but are not critical for the initial live tracking experience.

## Sources

- `frontend/src/pages/LiveMap.tsx`
- `frontend/src/pages/ShipHistory.tsx`
- `frontend/src/components/ShipList.tsx`
- `frontend/src/components/ShipPanel.tsx`
- `frontend/src/hooks/useShips.ts`
- `api/main.py`
- `data-sync/main.py`
