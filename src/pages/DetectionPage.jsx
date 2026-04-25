import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import CircularConfidence from '../components/CircularConfidence'
import RiskBadge from '../components/RiskBadge'
import { demoScenarios, timelineTemplate } from '../data/mock'

const tags = ['Urgency', 'External Link', 'Suspicious Domain', 'Low Reputation']

function DetectionPage() {
  const [payload, setPayload] = useState({ message_text: '', url: '', sender: '' })
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState(null)

  const canAnalyze = payload.message_text && payload.url && payload.sender

  const financial = useMemo(() => {
    if (!result) return { saved: 0, lost: 0, risk: 0 }
    return result.financial
  }, [result])

  const runAnalysis = () => {
    setIsLoading(true)
    setTimeout(() => {
      const suspicious = /urgent|verify|gift|confidential|blocked|charges/i.test(payload.message_text)
      const riskLevel = suspicious ? 'Fraud' : 'Safe'
      setResult({
        riskLevel,
        confidence: suspicious ? 94 : 81,
        explanation: suspicious
          ? [
              'Message uses urgency pressure to trigger rushed action.',
              'Sender identity is inconsistent with expected enterprise domain patterns.',
              'External destination exhibits risk signals (domain quality and intent mismatch).',
            ]
          : [
              'Communication pattern matches verified internal policy updates.',
              'Sender and URL context align with expected enterprise channels.',
              'No high-risk escalation cues detected in language or destination.',
            ],
        financial: suspicious ? { saved: 245000, lost: 18000, risk: 129000 } : { saved: 26000, lost: 0, risk: 8000 },
      })
      setIsLoading(false)
    }, 850)
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <section className="glass-card p-6">
        <p className="metric-label">Live Decision Sandbox</p>
        <h2 className="mt-3 text-2xl font-semibold text-white">Fraud chain simulation</h2>
        <div className="mt-6 space-y-4">
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">Message</span>
            <textarea
              rows={5}
              value={payload.message_text}
              onChange={(e) => setPayload((s) => ({ ...s, message_text: e.target.value }))}
              className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-3 text-sm text-white outline-none ring-accent/20 transition focus:ring"
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">URL</span>
            <input
              value={payload.url}
              onChange={(e) => setPayload((s) => ({ ...s, url: e.target.value }))}
              className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-3 text-sm text-white outline-none ring-accent/20 transition focus:ring"
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">Sender</span>
            <input
              value={payload.sender}
              onChange={(e) => setPayload((s) => ({ ...s, sender: e.target.value }))}
              className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-3 text-sm text-white outline-none ring-accent/20 transition focus:ring"
            />
          </label>

          <div className="flex flex-wrap gap-2">
            {demoScenarios.map((scenario) => (
              <button
                key={scenario.name}
                onClick={() => setPayload(scenario)}
                className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-slate-300 transition hover:scale-[1.02] hover:text-white"
              >
                {scenario.name}
              </button>
            ))}
          </div>

          <button
            disabled={!canAnalyze || isLoading}
            onClick={runAnalysis}
            className="w-full rounded-xl bg-accent px-4 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? 'Analyzing signals...' : 'Analyze Decision Chain'}
          </button>
        </div>
      </section>

      <section className="glass-card p-6">
        {!result ? (
          <div className="flex h-full min-h-96 items-center justify-center text-center text-sm text-slate-400">
            Submit a scenario to generate risk, reasoning, and financial impact.
          </div>
        ) : (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }}>
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div>
                <p className="metric-label">Risk Level</p>
                <div className="mt-2">
                  <RiskBadge level={result.riskLevel} />
                </div>
              </div>
              <CircularConfidence score={result.confidence} />
            </div>

            <div className="mt-6 grid gap-3 md:grid-cols-3">
              <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                <p className="metric-label">₹ Saved</p>
                <p className="mt-2 text-xl font-semibold text-emerald-300">₹{financial.saved.toLocaleString('en-IN')}</p>
              </div>
              <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                <p className="metric-label">₹ Lost</p>
                <p className="mt-2 text-xl font-semibold text-rose-300">₹{financial.lost.toLocaleString('en-IN')}</p>
              </div>
              <div className="rounded-xl border border-accent/30 bg-accent/10 p-4">
                <p className="metric-label">₹ At Risk</p>
                <p className="mt-2 text-xl font-semibold text-accent">₹{financial.risk.toLocaleString('en-IN')}</p>
              </div>
            </div>

            <div className="mt-6">
              <p className="metric-label">Detected Signals</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {tags.map((tag) => (
                  <span key={tag} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200">
                    {tag}
                  </span>
                ))}
              </div>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                <p className="metric-label">AI Reasoning</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-200">
                  {result.explanation.map((point) => (
                    <li key={point} className="flex gap-2">
                      <span className="text-accent">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                <p className="metric-label">Multi-step Chain</p>
                <ol className="mt-3 space-y-3 text-sm">
                  {timelineTemplate.map((item) => (
                    <li key={item.step} className="rounded-lg border border-white/10 bg-slate-900/45 p-3">
                      <div className="flex items-center justify-between">
                        <p className="font-medium text-white">Step {item.step} — {item.title}</p>
                        <RiskBadge level={item.status} />
                      </div>
                      <p className="mt-2 text-slate-300">{item.note}</p>
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          </motion.div>
        )}
      </section>
    </div>
  )
}

export default DetectionPage
