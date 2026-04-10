import { Routes, Route } from 'react-router-dom'
import LiveMap from './pages/LiveMap'
import ShipHistory from './pages/ShipHistory'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LiveMap />} />
      <Route path="/ships/:mmsi" element={<ShipHistory />} />
    </Routes>
  )
}
