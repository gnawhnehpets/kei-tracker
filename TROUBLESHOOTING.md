# Troubleshooting

## Ship history missing records

**Symptom:** The ship history endpoint did not return all historical records.

**Root cause:** The frontend's `fetchShipHistory` function hardcoded a `limit=500` query parameter, overriding the API's default of 5000 (max 10,000). Only 500 records were ever requested regardless of the available data.

**Fix:** Removed the `limit` parameter from the frontend (`frontend/src/api/client.ts`). The API's own default and max constraints (`default=5000, ge=1, le=10000` in `api/main.py`) now govern the result size.

## Ship track wrapping around the globe at the antimeridian

**Symptom:** When viewing a ship's history on the map, the track line drew a straight line across the entire world (through the Atlantic) instead of crossing the Pacific Ocean directly. This happened for ships whose route crossed the International Date Line (±180° longitude).

**Root cause:** Consecutive AIS position reports on either side of the antimeridian have longitudes that jump from e.g. `179°` to `−179°`. The `LineString` geometry treated these as a ~358° gap and rendered the line the long way around.

**Fix:** Added longitude unwrapping in `frontend/src/pages/ShipHistory.tsx`. When building the coordinate array, each point's longitude is adjusted by ±360° relative to the previous point so that the difference never exceeds 180°. MapLibre handles coordinates outside `[-180, 180]` correctly, so the track renders as a short crossing over the Pacific.
