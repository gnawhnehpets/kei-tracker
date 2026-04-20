import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'
import type { Ship } from '../api/client'

interface ShipMarkerProps {
  map: maplibregl.Map
  ship: Ship
  heading?: number
  onClick: (ship: Ship) => void
}

export default function ShipMarker({ map, ship, heading = 0, onClick }: ShipMarkerProps) {
  const markerRef = useRef<maplibregl.Marker | null>(null)

  useEffect(() => {
    const el = document.createElement('div')
    el.title = ship.ship_name.trim()
    el.style.cssText = `width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; cursor: pointer;`
    const isTarget = ship.mmsi === 257711000
    const fillColor = isTarget ? '#22c55e' : '#3b82f6'
    const strokeColor = isTarget ? '#16a34a' : '#1d4ed8'
    el.innerHTML = `<svg width="12" height="18" viewBox="0 0 12 18" xmlns="http://www.w3.org/2000/svg" style="transform: rotate(${heading}deg); transform-origin: 50% 50%; transition: transform 0.5s ease;">
      <polygon points="6,0 0,18 12,18" fill="${fillColor}" stroke="${strokeColor}" stroke-width="1.5"/>
    </svg>`
    el.addEventListener('click', () => onClick(ship))

    const marker = new maplibregl.Marker({ element: el, anchor: 'center' })
      .setLngLat([ship.last_longitude, ship.last_latitude])
      .addTo(map)

    markerRef.current = marker

    return () => {
      marker.remove()
    }
  }, [map])

  // Update position and heading when ship data changes
  useEffect(() => {
    if (!markerRef.current) return
    markerRef.current.setLngLat([ship.last_longitude, ship.last_latitude])
    const svg = markerRef.current.getElement().querySelector('svg')
    if (svg) svg.style.transform = `rotate(${heading}deg)`
  }, [ship.last_latitude, ship.last_longitude, heading])

  return null
}
