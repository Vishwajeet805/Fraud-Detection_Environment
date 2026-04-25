import { motion } from 'framer-motion'
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
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
          description="Monitor detection throughput, risk drift, and model certainty with production-level visibility."
        />
        <div className="grid gap-4 md:grid-cols-3">
          <StatCard label="Total checks" value="26,412" trend="+10.1% week over week" />
          <StatCard label="Fraud rate" value="16.9%" trend="Fraud spikes detected on Thu" />
          <StatCard label="Model accuracy" value="92.4%" trend="Model confidence stabilizing" />
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <motion.div className="glass-card p-5" initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
          <p className="metric-label">Fraud vs Safe trend</p>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dashboardSeries}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="date" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Line type="monotone" dataKey="fraud" stroke="#ff5f7d" strokeWidth={2.5} dot={false} />
                <Line type="monotone" dataKey="safe" stroke="#29d3ff" strokeWidth={2.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div className="glass-card p-5" initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
          <p className="metric-label">Confidence trend</p>
          <div className="mt-4 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={confidenceBuckets}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="bucket" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Bar dataKey="checks" fill="rgba(41, 211, 255, 0.72)" radius={[6, 6, 0, 0]} />
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
                  <RiskBadge level={row.prediction} />
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
