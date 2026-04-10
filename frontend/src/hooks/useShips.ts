import { useQuery } from '@tanstack/react-query'
import { fetchShips } from '../api/client'

export function useShips() {
  return useQuery({
    queryKey: ['ships'],
    queryFn: fetchShips,
    refetchInterval: 30_000,
  })
}
