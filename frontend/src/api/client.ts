const BASE = '/api'

export interface Ship {
  mmsi: number
  ship_name: string
  last_seen: string
  last_latitude: number
  last_longitude: number
  true_heading?: number
  cog?: number
}

export interface PositionRecord {
  _id: string
  Cog: number
  Latitude: number
  Longitude: number
  Sog: number
  TrueHeading: number
  NavigationalStatus: number
  MessageType: string
  MetaData: {
    MMSI: number
    ShipName: string
    latitude: number
    longitude: number
    time_utc: string
  }
  timestamp: string
}

export async function fetchShips(): Promise<Ship[]> {
  const res = await fetch(`${BASE}/ships`)
  if (!res.ok) throw new Error('Failed to fetch ships')
  const data = await res.json()
  return data.ships
}

export async function fetchShipHistory(
  mmsi: number,
  since?: string,
  limit = 500,
): Promise<PositionRecord[]> {
  const params = new URLSearchParams({
    limit: String(limit),
    message_type: 'PositionReport',
  })
  if (since) params.set('since', since)
  const res = await fetch(`${BASE}/ships/${mmsi}/history?${params}`)
  // Some time windows legitimately have no records; treat 404 as empty history.
  if (res.status === 404) return []
  if (!res.ok) throw new Error('Failed to fetch ship history')
  const data = await res.json()
  return data.records
}

export async function fetchShipLatest(mmsi: number): Promise<PositionRecord> {
  const res = await fetch(`${BASE}/ships/${mmsi}/latest`)
  if (!res.ok) throw new Error('Failed to fetch latest position')
  return res.json()
}
