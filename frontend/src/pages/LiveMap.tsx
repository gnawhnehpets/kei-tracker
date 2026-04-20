import { useState, useCallback, useEffect } from 'react'
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
        ships={ships}
        selectedMmsi={selected?.mmsi}
        onSelect={handleSelect}
      />

      <div className="absolute inset-0 left-64">
        <Map onMapReady={setMap} center={[15, 60]} zoom={4}>
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
