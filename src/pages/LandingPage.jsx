import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import SectionHeader from '../components/SectionHeader'

const features = [
  {
    title: 'Real-time fraud detection',
    text: 'Analyze messages, URLs, and sender behavior in one low-latency decision surface.',
  },
  {
    title: 'Sequential risk modeling',
    text: 'Track fraud progression across multiple AI decision steps before taking action.',
  },
  {
    title: 'Explainable AI reasoning',
    text: 'Every decision includes concise reasoning and traceable signals for audit confidence.',
  },
  {
    title: 'Financial impact simulation',
    text: 'Estimate saved capital, active exposure, and potential loss before fraud events escalate.',
  },
]

function LandingPage() {
  return (
    <div className="space-y-16 pb-10">
      <section className="glass-card relative overflow-hidden px-8 py-16 md:px-12">
        <motion.div
          animate={{ opacity: [0.25, 0.45, 0.25] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-accent/10 via-cyan-400/5 to-transparent"
        />
        <div className="relative">
          <p className="metric-label">Enterprise Fraud Operations</p>
          <h2 className="mt-3 max-w-3xl text-4xl font-semibold tracking-tight text-white md:text-5xl">
            AI Fraud Decision Intelligence
          </h2>
          <p className="mt-5 max-w-2xl text-base text-slate-300 md:text-lg">
            Deploy multi-step AI analysis to identify fraudulent intent, explain every decision path, and quantify
            financial exposure before losses compound.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              to="/detect"
              className="rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.02]"
            >
              Try Live Demo
            </Link>
            <Link
              to="/dashboard"
              className="rounded-xl border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:scale-[1.02]"
            >
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section>
        <SectionHeader
          eyebrow="Platform Capabilities"
          title="Designed for decision velocity, not static scoring"
          description="Built to mirror fintech-grade fraud operations where model output, reasoning, and capital impact are reviewed in one workflow."
        />

        <div className="grid gap-4 md:grid-cols-2">
          {features.map((feature, idx) => (
            <motion.article
              key={feature.title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.35, delay: idx * 0.05 }}
              className="glass-card p-6"
            >
              <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
              <p className="mt-2 text-sm text-slate-300">{feature.text}</p>
            </motion.article>
          ))}
        </div>
      </section>
    </div>
  )
}

export default LandingPage
