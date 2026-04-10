import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import type { PositionRecord } from '../api/client'

interface SpeedChartProps {
  records: PositionRecord[]
}

export default function SpeedChart({ records }: SpeedChartProps) {
  const data = [...records]
    .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
    .map((r) => ({
      time: new Date(r.timestamp).toLocaleTimeString(),
      sog: r.Sog,
      cog: r.Cog,
    }))

  return (
    <div className="bg-gray-900 rounded-xl p-4 border border-gray-700">
      <h3 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
        Speed & Course Over Ground
      </h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis
            dataKey="time"
            tick={{ fill: '#9ca3af', fontSize: 11 }}
            interval="preserveStartEnd"
          />
          <YAxis yAxisId="sog" tick={{ fill: '#9ca3af', fontSize: 11 }} unit=" kn" width={48} />
          <YAxis
            yAxisId="cog"
            orientation="right"
            tick={{ fill: '#9ca3af', fontSize: 11 }}
            unit="°"
            width={40}
          />
          <Tooltip
            contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }}
            labelStyle={{ color: '#d1d5db' }}
          />
          <Legend wrapperStyle={{ color: '#d1d5db', fontSize: 12 }} />
          <Line
            yAxisId="sog"
            type="monotone"
            dataKey="sog"
            stroke="#3b82f6"
            dot={false}
            strokeWidth={2}
            name="SOG (kn)"
          />
          <Line
            yAxisId="cog"
            type="monotone"
            dataKey="cog"
            stroke="#10b981"
            dot={false}
            strokeWidth={2}
            name="COG (°)"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
