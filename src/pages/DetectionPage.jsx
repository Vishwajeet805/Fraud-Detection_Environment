import { useEffect, useMemo, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import CircularConfidence from '../components/CircularConfidence'
import RiskBadge from '../components/RiskBadge'
import { demoScenarios } from '../data/mock'

const analysisSteps = [
  'Parsing message...',
  'Extracting features...',
  'Evaluating sender...',
  'Analyzing risk patterns...',
  'Generating decision...',
]

function CountValue({ value }) {
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    let frame
    let current = 0
    const step = Math.max(1, Math.round(value / 40))

    const tick = () => {
      current += step
      if (current >= value) {
        setDisplay(value)
        return
      }
      setDisplay(current)
      frame = window.setTimeout(tick, 22)
    }

    setDisplay(0)
    tick()

    return () => window.clearTimeout(frame)
  }, [value])

  return <>{display.toLocaleString('en-IN')}</>
}

function DetectionPage() {
  const [payload, setPayload] = useState({ message_text: '', url: '', sender: '' })
  const [isLoading, setIsLoading] = useState(false)
  const [activeStep, setActiveStep] = useState(-1)
  const [result, setResult] = useState(null)

  const canAnalyze = payload.message_text.trim().length > 0

  const BASE_URL = "";

  const runAnalysis = async () => {
  if (!canAnalyze || isLoading) return

  setResult(null)
  setIsLoading(true)
  setActiveStep(-1)

  try {
    // Reset environment — send user payload
    await fetch(`${BASE_URL}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message_text: payload.message_text,
        url: payload.url,
        sender: payload.sender,
      }),
    })

    // Animate thinking steps
    analysisSteps.forEach((_, index) => {
      window.setTimeout(() => setActiveStep(index), index * 340)
    })

    // Determine action from message content (simple heuristic for UI)
    const msg = payload.message_text.toLowerCase()
    const fraudWords = ['otp', 'pin', 'urgent', 'won', 'prize', 'blocked',
                        'click here', 'verify', 'expire', 'immediately',
                        'aadhaar', 'pan', 'loan', 'fee', 'transfer']
    const fraudScore = fraudWords.filter(w => msg.includes(w)).length
    const action = fraudScore >= 3 ? 1 : fraudScore >= 1 ? 2 : 0

    // Call step with determined action
    const stepResponse = await fetch(`${BASE_URL}/step`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    })

    if (!stepResponse.ok) {
      throw new Error(`Server error: ${stepResponse.status}`)
    }

    const stepData = await stepResponse.json()

    // ── Map backend fields to UI — NO hardcoded values ──────────────────

    // Risk level from backend label (0=Safe, 1=Fraud, 2=Suspicious)
    const label = stepData.info?.label ?? action
    const riskLevel = label === 0 ? 'Safe' : label === 1 ? 'Fraud' : 'Suspicious'

    // Confidence from reward total (shaped to 1–99%)
    const rewardTotal = stepData.reward?.total ?? 0
    const absReward = Math.abs(rewardTotal)
    const confidence = Math.min(99, Math.max(1, Math.round(absReward * 40 + 55)))

    // Signals from backend obs_explanation array
    const signals = Array.isArray(stepData.info?.obs_explanation)
      ? stepData.info.obs_explanation
      : ['Analysis complete']

    // Explanation from backend explanation_text
    const explanationText = stepData.info?.explanation_text
      || stepData.info?.explanation
      || 'Decision made based on message analysis'
    const explanation = [explanationText]

    // Financial from backend — these are the real values, never hardcoded
    const financial = {
      saved:         stepData.info?.money_saved   ?? 0,
      risk:          stepData.info?.money_at_risk  ?? 0,
      potentialLoss: stepData.info?.money_lost     ?? 0,
    }

    setResult({ riskLevel, confidence, signals, explanation, financial })

  } catch (error) {
    console.error('Analysis failed:', error)
    setResult({
      riskLevel: 'Error',
      confidence: 0,
      signals: ['Connection failed — is the server running?'],
      explanation: [error.message || 'Unable to complete analysis. Please try again.'],
      financial: { saved: 0, risk: 0, potentialLoss: 0 },
    })
  } finally {
    setIsLoading(false)
  }
}

  const financial = useMemo(() => result?.financial ?? { saved: 0, risk: 0, potentialLoss: 0 }, [result])

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_1.1fr]">
      <section className="glass-card p-6">
        <p className="metric-label">Live Decision Sandbox</p>
        <h2 className="mt-3 text-2xl font-semibold text-white">Fraud chain simulation</h2>
        <p className="mt-2 text-sm text-slate-300">Enter only message text to run. URL and sender are optional context.</p>

        <div className="mt-6 space-y-4">
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">Message *</span>
            <textarea
              rows={5}
              value={payload.message_text}
              onChange={(e) => setPayload((prev) => ({ ...prev, message_text: e.target.value }))}
              placeholder="Paste message content here..."
              className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-3 text-sm text-white outline-none ring-accent/20 transition focus:ring"
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">URL (optional)</span>
            <input
              value={payload.url}
              onChange={(e) => setPayload((prev) => ({ ...prev, url: e.target.value }))}
              className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-3 text-sm text-white outline-none ring-accent/20 transition focus:ring"
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-sm text-slate-300">Sender (optional)</span>
            <input
              value={payload.sender}
              onChange={(e) => setPayload((prev) => ({ ...prev, sender: e.target.value }))}
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
            {isLoading ? 'Analyzing decision process...' : 'Analyze'}
          </button>
        </div>
      </section>

      <section className="glass-card p-6">
        <p className="metric-label">AI Thinking Engine</p>
        <div className="mt-4 space-y-3">
          {analysisSteps.map((step, index) => {
            const active = index <= activeStep
            return (
              <motion.div
                key={step}
                initial={{ opacity: 0.35, x: -8 }}
                animate={{ opacity: active ? 1 : 0.35, x: active ? 0 : -8 }}
                className={`rounded-xl border p-3 text-sm transition ${
                  active ? 'border-accent/30 bg-accent/10 text-slate-100' : 'border-white/10 bg-white/5 text-slate-400'
                }`}
              >
                <span className="mr-2 text-xs text-accentSoft">0{index + 1}</span>
                {step}
              </motion.div>
            )
          })}
        </div>

        <AnimatePresence>
          {result ? (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 8 }}
              transition={{ duration: 0.3 }}
              className="mt-6"
            >
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
                  <p className="mt-2 text-xl font-semibold text-accent">₹<CountValue value={financial.saved} /></p>
                </div>
                <div className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <p className="metric-label">₹ At Risk</p>
                  <p className="mt-2 text-xl font-semibold text-warning">₹<CountValue value={financial.risk} /></p>
                </div>
                <div className="rounded-xl border border-danger/30 bg-danger/10 p-4">
                  <p className="metric-label">₹ Potential Loss</p>
                  <p className="mt-2 text-xl font-semibold text-danger">₹<CountValue value={financial.potentialLoss} /></p>
                </div>
              </div>

              <div className="mt-6">
                <p className="metric-label">Detected Signals</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {result.signals.map((tag) => (
                    <span key={tag} className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-200">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mt-6 rounded-xl border border-white/10 bg-white/5 p-4">
                <p className="metric-label">Explanation</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-200">
                  {result.explanation.map((point) => (
                    <li key={point} className="flex gap-2">
                      <span className="text-accent">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ) : (
            <div className="mt-8 rounded-xl border border-dashed border-white/15 p-8 text-center text-sm text-slate-400">
              Run an analysis to render the final decision, confidence, reasoning, and financial consequence model.
            </div>
          )}
        </AnimatePresence>
      </section>
    </div>
  )
}

export default DetectionPage
