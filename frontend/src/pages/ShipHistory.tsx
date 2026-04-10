import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import maplibregl from 'maplibre-gl'
import Map from '../components/Map'
import SpeedChart from '../components/SpeedChart'
import { useShipHistory } from '../hooks/useShipHistory'

const RANGES = [
  { label: '1 h', hours: 1 },
  { label: '6 h', hours: 6 },
  { label: '24 h', hours: 24 },
  { label: 'All', hours: 0 },
]

export default function ShipHistory() {
  const { mmsi } = useParams<{ mmsi: string }>()
  const navigate = useNavigate()
  const [rangeHours, setRangeHours] = useState(6)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const sourceAdded = useRef(false)

  const since =
    rangeHours > 0
      ? new Date(Date.now() - rangeHours * 3_600_000).toISOString()
      : undefined

  const { data: records = [], isLoading } = useShipHistory(Number(mmsi), since)

  const shipName = records[0]?.MetaData?.ShipName?.trim() || `MMSI ${mmsi}`

  // Draw track on map whenever records change
  useEffect(() => {
    const map = mapRef.current
    if (!map || records.length === 0) return

    const coords: [number, number][] = [...records]
      .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
      .map((r) => [r.Longitude, r.Latitude])

    const geojson: GeoJSON.FeatureCollection = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: { type: 'LineString', coordinates: coords },
          properties: {},
        },
        ...coords.map((c, i) => ({
          type: 'Feature' as const,
          geometry: { type: 'Point' as const, coordinates: c },
          properties: { index: i, total: coords.length },
        })),
      ],
    }

    if (sourceAdded.current) {
      const src = map.getSource('track') as maplibregl.GeoJSONSource | undefined
      src?.setData(geojson)
    } else {
      map.addSource('track', { type: 'geojson', data: geojson })
      map.addLayer({
        id: 'track-line',
        type: 'line',
        source: 'track',
        filter: ['==', '$type', 'LineString'],
        paint: {
          'line-color': '#3b82f6',
          'line-width': 2,
          'line-opacity': 0.8,
        },
      })
      map.addLayer({
        id: 'track-points',
        type: 'circle',
        source: 'track',
        filter: ['==', '$type', 'Point'],
        paint: {
          'circle-radius': 3,
          'circle-color': '#60a5fa',
          'circle-opacity': 0.7,
        },
      })
      sourceAdded.current = true
    }

    // Fit map to track
    if (coords.length > 1) {
      const bounds = coords.reduce(
        (b, c) => b.extend(c as [number, number]),
        new maplibregl.LngLatBounds(coords[0], coords[0]),
      )
      map.fitBounds(bounds, { padding: 60, maxZoom: 12 })
    }
  }, [records])

  function handleMapReady(map: maplibregl.Map) {
    mapRef.current = map
  }

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-white">
      {/* Header */}
      <div className="flex items-center gap-4 px-6 py-3 bg-gray-900 border-b border-gray-700 shrink-0">
        <button
          onClick={() => navigate('/')}
          className="text-gray-400 hover:text-white text-sm transition"
        >
          ← Live map
        </button>
        <div>
          <h1 className="font-semibold">{shipName}</h1>
          <p className="text-xs text-gray-400">MMSI: {mmsi}</p>
        </div>

        {/* Time range selector */}
        <div className="ml-auto flex gap-1">
          {RANGES.map((r) => (
            <button
              key={r.label}
              onClick={() => setRangeHours(r.hours)}
              className={`px-3 py-1 rounded-lg text-sm transition ${
                rangeHours === r.hours
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {r.label}
            </button>
          ))}
        </div>
      </div>

      {/* Map */}
      <div className="flex-1 min-h-0">
        {isLoading && (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-400 text-sm">Loading track…</p>
          </div>
        )}
        {!isLoading && (
          <Map onMapReady={handleMapReady} center={[15, 60]} zoom={5} className="h-full" />
        )}
      </div>

      {/* Charts */}
      {records.length > 0 && (
        <div className="shrink-0 p-4 bg-gray-950 border-t border-gray-700">
          <SpeedChart records={records} />
          <p className="text-xs text-gray-500 mt-2 text-right">{records.length} position records</p>
        </div>
      )}
    </div>
  )
}
