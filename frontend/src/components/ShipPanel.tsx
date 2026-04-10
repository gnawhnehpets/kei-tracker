import { useNavigate } from 'react-router-dom'
import type { Ship } from '../api/client'

const NAV_STATUS: Record<number, string> = {
  0: 'Under way (engine)',
  1: 'At anchor',
  2: 'Not under command',
  3: 'Restricted manoeuvrability',
  5: 'Moored',
  8: 'Sailing',
  15: 'Unknown',
}

interface ShipPanelProps {
  ship: Ship
  sog?: number
  cog?: number
  navStatus?: number
  onClose: () => void
}

export default function ShipPanel({ ship, sog, cog, navStatus, onClose }: ShipPanelProps) {
  const navigate = useNavigate()

  return (
    <div className="absolute top-4 right-14 z-10 w-72 bg-gray-900 text-white rounded-xl shadow-2xl p-4 border border-gray-700">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h2 className="text-lg font-semibold leading-tight">{ship.ship_name.trim()}</h2>
          <p className="text-xs text-gray-400">MMSI: {ship.mmsi}</p>
        </div>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white text-xl leading-none"
          aria-label="Close"
        >
          ×
        </button>
      </div>

      <div className="grid grid-cols-2 gap-2 text-sm mb-4">
        <Stat label="SOG" value={sog !== undefined ? `${sog.toFixed(1)} kn` : '—'} />
        <Stat label="COG" value={cog !== undefined ? `${cog.toFixed(1)}°` : '—'} />
        <Stat
          label="Status"
          value={navStatus !== undefined ? (NAV_STATUS[navStatus] ?? `Code ${navStatus}`) : '—'}
          wide
        />
        <Stat
          label="Last seen"
          value={new Date(ship.last_seen).toLocaleTimeString()}
        />
      </div>

      <button
        onClick={() => navigate(`/ships/${ship.mmsi}`)}
        className="w-full bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium py-2 rounded-lg transition"
      >
        View history →
      </button>
    </div>
  )
}

function Stat({ label, value, wide = false }: { label: string; value: string; wide?: boolean }) {
  return (
    <div className={`bg-gray-800 rounded-lg p-2 ${wide ? 'col-span-2' : ''}`}>
      <p className="text-xs text-gray-400 uppercase tracking-wide">{label}</p>
      <p className="font-medium truncate">{value}</p>
    </div>
  )
}
