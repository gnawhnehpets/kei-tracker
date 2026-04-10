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
    el.className = 'ship-marker'
    el.title = ship.ship_name.trim()
    el.style.cssText = `
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-bottom: 18px solid #3b82f6;
      transform: rotate(${heading}deg);
      cursor: pointer;
      filter: drop-shadow(0 1px 2px rgba(0,0,0,0.5));
      transition: transform 0.5s ease;
    `
    el.addEventListener('click', () => onClick(ship))

    const marker = new maplibregl.Marker({ element: el })
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
    const el = markerRef.current.getElement()
    el.style.transform = `rotate(${heading}deg)`
  }, [ship.last_latitude, ship.last_longitude, heading])

  return null
}
