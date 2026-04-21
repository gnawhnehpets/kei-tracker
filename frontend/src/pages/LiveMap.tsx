import { useState, useCallback, useEffect, useMemo } from 'react'
import maplibregl from 'maplibre-gl'
import Map from '../components/Map'
import ShipMarker from '../components/ShipMarker'
import ShipList from '../components/ShipList'
import ShipPanel from '../components/ShipPanel'
import { useShips } from '../hooks/useShips'
import type { Ship } from '../api/client'

export default function LiveMap() {
  const { data: ships = [], isLoading } = useShips()
  const [map, setMap] = useState<maplibregl.Map | null>(null)
  const [selected, setSelected] = useState<Ship | null>(null)

  // Sort ships: 257711000 first, then rest by last_seen
  const sortedShips = useMemo(() => {
    const targetShip = ships.find(s => s.mmsi === 257711000)
    const others = ships.filter(s => s.mmsi !== 257711000)
    return targetShip ? [targetShip, ...others] : ships
  }, [ships])

  // Auto-select ship 257711000 on initial load
  useEffect(() => {
    if (ships.length > 0 && !selected) {
      const targetShip = ships.find(s => s.mmsi === 257711000) || ships[0]
      setSelected(targetShip)
    }
  }, [ships, selected])

  // Fly map to selected ship
  useEffect(() => {
    if (selected && map) {
      map.flyTo({ center: [selected.last_longitude, selected.last_latitude], zoom: 8 })
    }
  }, [selected, map])

  // Create GeoJSON for text labels and add layer
  useEffect(() => {
    if (!map || ships.length === 0) return

    const geojson: GeoJSON.FeatureCollection = {
      type: 'FeatureCollection',
      features: ships.map(ship => ({
        type: 'Feature' as const,
        geometry: {
          type: 'Point' as const,
          coordinates: [ship.last_longitude, ship.last_latitude],
        },
        properties: {
          ship_name: ship.ship_name.trim() || `MMSI ${ship.mmsi}`,
          latitude: ship.last_latitude.toFixed(4),
          longitude: ship.last_longitude.toFixed(4),
        },
      })),
    }

    // Update or create source
    const source = map.getSource('ship-labels') as maplibregl.GeoJSONSource | undefined
    if (source) {
      source.setData(geojson)
    } else {
      map.addSource('ship-labels', { type: 'geojson', data: geojson })

      // Add text labels (only visible at zoom 9+)
      map.addLayer({
        id: 'ship-labels-layer',
        type: 'symbol',
        source: 'ship-labels',
        minzoom: 9,
        layout: {
          'text-field': ['format', ['get', 'ship_name'], { 'font-scale': 0.9 }, '\n', {}, ['get', 'latitude'], { 'font-scale': 0.75 }, ' ', {}, ['get', 'longitude'], { 'font-scale': 0.75 }],
          'text-offset': [0, 1.5],
          'text-size': 11,
          'text-anchor': 'top',
          'text-allow-overlap': false,
          'text-max-width': 8,
        },
        paint: {
          'text-color': '#e5e7eb',
          'text-halo-color': '#1f2937',
          'text-halo-width': 1.5,
        },
      })
    }
  }, [map, ships])

  const handleSelect = useCallback(
    (ship: Ship) => {
      setSelected(ship)
      map?.flyTo({ center: [ship.last_longitude, ship.last_latitude], zoom: 8 })
    },
    [map],
  )

  return (
    <div className="relative w-full h-screen bg-gray-950">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center z-20 bg-gray-950">
          <p className="text-white text-sm">Loading ships…</p>
        </div>
      )}

      <ShipList
        ships={sortedShips}
        selectedMmsi={selected?.mmsi}
        onSelect={handleSelect}
      />

      <div className="absolute inset-0 left-64">
        <Map onMapReady={setMap} center={[138, 36]} zoom={5}>
          {() => null}
        </Map>

        {map &&
          ships.map((ship) => (
            <ShipMarker
              key={ship.mmsi}
              map={map}
              ship={ship}
              heading={ship.true_heading != null && ship.true_heading !== 511 ? ship.true_heading : (ship.cog ?? 0)}
              onClick={handleSelect}
            />
          ))}
      </div>

      {selected && (
        <ShipPanel
          ship={selected}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  )
}
