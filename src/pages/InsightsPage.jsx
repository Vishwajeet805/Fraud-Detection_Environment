import { motion } from 'framer-motion'
import { Area, AreaChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import SectionHeader from '../components/SectionHeader'
import { rewardCurve } from '../data/mock'

function InsightsPage() {
  return (
    <div className="space-y-8 pb-8">
      <SectionHeader
        eyebrow="Training Intelligence"
        title="Agent improves decision-making over time"
        description="Agent improves decision-making over time using reward feedback from each completed fraud decision episode."
      />

      <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <motion.section className="glass-card p-5" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
          <p className="metric-label">Reward curve (episode vs reward)</p>
          <div className="mt-4 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={rewardCurve}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                <XAxis dataKey="episode" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                <Line type="monotone" dataKey="baseline" name="Before" stroke="#7c8cff" strokeWidth={2} />
                <Line type="monotone" dataKey="improved" name="After" stroke="#29d3ff" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.section>

        <section className="space-y-4">
          <div className="glass-card p-5">
            <p className="metric-label">Before vs After</p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                <p className="text-xs text-slate-400">Before</p>
                <p className="mt-2 text-2xl font-semibold text-accentSoft">49%</p>
                <p className="mt-1 text-xs text-slate-400">Successful interception</p>
              </div>
              <div className="rounded-xl border border-accent/30 bg-accent/10 p-3">
                <p className="text-xs text-slate-300">After</p>
                <p className="mt-2 text-2xl font-semibold text-accent">87%</p>
                <p className="mt-1 text-xs text-slate-300">Successful interception</p>
              </div>
            </div>
          </div>

          <div className="glass-card p-5">
            <p className="metric-label">Success rate increase</p>
            <div className="mt-4 h-40">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={rewardCurve}>
                  <defs>
                    <linearGradient id="reward-fill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="rgba(41,211,255,0.4)" />
                      <stop offset="100%" stopColor="rgba(41,211,255,0.04)" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.1)" />
                  <XAxis dataKey="episode" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ background: '#111827', border: '1px solid rgba(255,255,255,0.1)' }} />
                  <Area type="monotone" dataKey="improved" stroke="#29d3ff" fill="url(#reward-fill)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export default InsightsPage
