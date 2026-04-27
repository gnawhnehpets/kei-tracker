import { useState, useEffect, useRef, useMemo } from 'react'
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
  const shipMarkerRef = useRef<maplibregl.Marker | null>(null)
  const [mapReady, setMapReady] = useState(false)

  const since = useMemo(
    () =>
      rangeHours > 0
        ? new Date(Date.now() - rangeHours * 3_600_000).toISOString()
        : undefined,
    [rangeHours],
  )

  const { data: records = [], isLoading, isFetching } = useShipHistory(Number(mmsi), since)

  const shipName = records[0]?.MetaData?.ShipName?.trim() || `MMSI ${mmsi}`

  // Derive initial map center from the latest record so we don't start at a default location
  const initialCenter = useMemo((): [number, number] => {
    if (records.length === 0) return [135, 35] // fallback: Japan
    const latest = [...records].sort(
      (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime(),
    )[0]
    return [latest.Longitude, latest.Latitude]
  }, [records.length > 0])

  // Draw track on map whenever records or map readiness changes
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapReady) return

    if (records.length === 0) {
      try {
        if (map.getLayer('track-line')) map.removeLayer('track-line')
        if (map.getLayer('track-points')) map.removeLayer('track-points')
        if (map.getSource('track')) map.removeSource('track')
      } catch {
        // Map may be transitioning; ignore and retry on next render.
      }
      shipMarkerRef.current?.remove()
      shipMarkerRef.current = null
      sourceAdded.current = false
      return
    }

    const sortedRecords = [...records].sort(
      (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    )
    const coords: [number, number][] = sortedRecords.map((r) => [r.Longitude, r.Latitude])

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

    try {
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
    } catch {
      return
    }

    // Fit map to track instantly (no animation — map initializes at correct center already)
    if (coords.length > 1) {
      const bounds = coords.reduce(
        (b, c) => b.extend(c as [number, number]),
        new maplibregl.LngLatBounds(coords[0], coords[0]),
      )
      map.fitBounds(bounds, { padding: 60, maxZoom: 12, animate: false })
    }

    // Place / update ship icon at the latest coordinate
    const latest = coords[coords.length - 1]
    const latestRecord = sortedRecords[sortedRecords.length - 1]
    const heading = latestRecord?.TrueHeading != null && latestRecord.TrueHeading !== 511
      ? latestRecord.TrueHeading
      : (latestRecord?.Cog ?? 0)

    if (shipMarkerRef.current) {
      shipMarkerRef.current.setLngLat(latest)
      const svg = shipMarkerRef.current.getElement().querySelector('svg')
      if (svg) svg.style.transform = `rotate(${heading}deg)`
    } else {
      const el = document.createElement('div')
      el.title = shipName
      el.style.cssText = `width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;`
      el.innerHTML = `<svg width="14" height="20" viewBox="0 0 14 20" xmlns="http://www.w3.org/2000/svg" style="transform: rotate(${heading}deg); transform-origin: 50% 50%; transition: transform 0.5s ease;">
        <polygon points="7,0 0,20 14,20" fill="#f59e0b" stroke="#92400e" stroke-width="1.5"/>
      </svg>`
      shipMarkerRef.current = new maplibregl.Marker({ element: el, anchor: 'center' })
        .setLngLat(latest)
        .addTo(map)
    }
  }, [records, mapReady])

  function handleMapReady(map: maplibregl.Map) {
    mapRef.current = map
    setMapReady(true)
  }

  // Clean up marker on unmount
  useEffect(() => {
    return () => {
      shipMarkerRef.current?.remove()
    }
  }, [])

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

      {/* Keep map mounted across filter changes to avoid stale map/source references */}
      <div className="relative flex-1 min-h-0">
        <Map onMapReady={handleMapReady} center={initialCenter} zoom={7} className="h-full" />
        {(isLoading || isFetching) && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-950/55 pointer-events-none">
            <p className="text-gray-300 text-sm">Loading track…</p>
          </div>
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
