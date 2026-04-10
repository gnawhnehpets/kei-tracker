import { useQuery } from '@tanstack/react-query'
import { fetchShipHistory } from '../api/client'

export function useShipHistory(mmsi: number, since?: string) {
  return useQuery({
    queryKey: ['shipHistory', mmsi, since],
    queryFn: () => fetchShipHistory(mmsi, since),
    enabled: !!mmsi,
  })
}
