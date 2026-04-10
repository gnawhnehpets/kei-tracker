import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'

interface MapProps {
  children?: (map: maplibregl.Map) => React.ReactNode
  onMapReady?: (map: maplibregl.Map) => void
  center?: [number, number]
  zoom?: number
  className?: string
}

export default function Map({ onMapReady, center = [15, 60], zoom = 4, className = '' }: MapProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: 'https://tiles.openfreemap.org/styles/liberty',
      center,
      zoom,
    })

    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    map.addControl(new maplibregl.ScaleControl(), 'bottom-left')

    map.on('load', () => {
      onMapReady?.(map)
    })

    mapRef.current = map

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [])

  return <div ref={containerRef} className={`w-full h-full ${className}`} />
}

export type { maplibregl }
