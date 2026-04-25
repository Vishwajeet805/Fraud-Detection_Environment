import { motion } from 'framer-motion'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import SectionHeader from '../components/SectionHeader'
import StatCard from '../components/StatCard'
import { activityRows, confidenceBuckets, dashboardSeries } from '../data/mock'
import RiskBadge from '../components/RiskBadge'

function DashboardPage() {
  return (
    <div className="space-y-10 pb-8">
      <section>
        <SectionHeader
          eyebrow="Operations Analytics"
          title="Fraud command center"
          description="Monitor detection volume, model confidence, and decision quality from a single operational dashboard."
        />
        <div className="grid gap-4 md:grid-cols-3">
          <StatCard label="Total checks" value="24,892" trend="+8.2% vs last week" />
          <StatCard label="Fraud rate" value="18.4%" trend="-2.1% false positives" />
          <StatCard label="Avg confidence" value="86.7%" trend="+4.8 model calibration" />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <motion.div className="glass-card p-5" initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
          <p className="metric-label">Fraud vs Safe over time</p>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dashboardSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="date" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Legend />
                <Line type="monotone" dataKey="fraud" stroke="#f97316" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="safe" stroke="#1dd4bf" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div className="glass-card p-5" initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
          <p className="metric-label">Confidence distribution</p>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={confidenceBuckets}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="bucket" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Bar dataKey="checks" fill="rgba(29, 212, 191, 0.7)" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </section>

      <section className="glass-card overflow-hidden">
        <div className="border-b border-white/10 px-5 py-4">
          <p className="metric-label">Recent activity</p>
        </div>
        <table className="w-full text-left text-sm">
          <thead className="text-slate-400">
            <tr>
              <th className="px-5 py-3 font-medium">Message</th>
              <th className="px-5 py-3 font-medium">Prediction</th>
              <th className="px-5 py-3 font-medium">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {activityRows.map((row) => (
              <tr key={row.message} className="border-t border-white/5">
                <td className="px-5 py-3 text-slate-200">{row.message}</td>
                <td className="px-5 py-3">
                  <RiskBadge level={row.prediction === 'Suspicious' ? 'Suspicious' : row.prediction} />
                </td>
                <td className="px-5 py-3 text-slate-300">{row.confidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  )
}

export default DashboardPage
