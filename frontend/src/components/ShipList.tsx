import type { Ship } from '../api/client'

interface ShipListProps {
  ships: Ship[]
  selectedMmsi?: number
  onSelect: (ship: Ship) => void
}

export default function ShipList({ ships, selectedMmsi, onSelect }: ShipListProps) {
  return (
    <div className="absolute top-0 left-0 h-full w-64 bg-gray-900/90 backdrop-blur text-white z-10 flex flex-col border-r border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-lg font-bold tracking-wide">Kei Tracker</h1>
        <p className="text-xs text-gray-400">{ships.length} vessel{ships.length !== 1 ? 's' : ''} tracked</p>
      </div>
      <ul className="overflow-y-auto flex-1 divide-y divide-gray-800">
        {ships.map((ship) => (
          <li key={ship.mmsi}>
            <button
              onClick={() => onSelect(ship)}
              className={`w-full text-left px-4 py-3 hover:bg-gray-700 transition ${
                selectedMmsi === ship.mmsi ? 'bg-gray-700 border-l-2 border-blue-500' : ''
              }`}
            >
              <p className="font-medium text-sm truncate">{ship.ship_name.trim() || 'Unknown'}</p>
              <p className="text-xs text-gray-400">MMSI: {ship.mmsi}</p>
              <p className="text-xs text-gray-500">
                {new Date(ship.last_seen).toLocaleString()}
              </p>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
