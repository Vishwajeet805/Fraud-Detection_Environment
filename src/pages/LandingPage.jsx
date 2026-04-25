import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import SectionHeader from '../components/SectionHeader'

const features = [
  {
    title: 'Real-time fraud detection',
    text: 'Low-latency scoring continuously evaluates messages, links, and sender context as incidents unfold.',
  },
  {
    title: 'Multi-step reasoning',
    text: 'A deterministic decision chain reveals how the agent parses signals before classifying risk.',
  },
  {
    title: 'Explainable AI',
    text: 'Every output includes auditable evidence and traceable rationale for analyst sign-off.',
  },
  {
    title: 'Financial impact awareness',
    text: 'Capital exposure and potential prevention outcomes are surfaced in the same decision surface.',
  },
]

function LandingPage() {
  return (
    <div className="space-y-16 pb-10">
      <section className="gradient-section glass-card relative overflow-hidden px-8 py-16 md:px-12">
        <motion.div
          animate={{ opacity: [0.18, 0.34, 0.18] }}
          transition={{ duration: 9, repeat: Infinity, ease: 'easeInOut' }}
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-accent/10 via-accentSoft/10 to-transparent"
        />
        <div className="relative">
          <p className="metric-label">Enterprise Fraud Operations</p>
          <h2 className="mt-3 max-w-3xl text-4xl font-semibold tracking-tight text-white md:text-5xl">
            AI Fraud Decision Intelligence
          </h2>
          <p className="mt-5 max-w-2xl text-base text-slate-300 md:text-lg">
            Real-time agentic reasoning for fraud prevention. See how risk evolves, why decisions are made, and what
            financial outcomes are at stake before damage compounds.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              to="/detect"
              className="rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.02]"
            >
              Try Demo
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
          eyebrow="Core Capabilities"
          title="Designed for precision-led fraud operations"
          description="The product experience mirrors modern fintech and cybersecurity teams where explainability and actionability matter as much as model output."
        />

        <div className="grid gap-4 md:grid-cols-2">
          {features.map((feature, idx) => (
            <motion.article
              key={feature.title}
              initial={{ opacity: 0, y: 14 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.4 }}
              transition={{ duration: 0.35, delay: idx * 0.06 }}
              whileHover={{ y: -2 }}
              className="glass-card p-6"
            >
              <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
              <p className="mt-2 text-sm text-slate-300">{feature.text}</p>
            </motion.article>
          ))}
        </div>
      </section>

      <motion.section
        className="gradient-section glass-card p-8"
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.35 }}
        transition={{ duration: 0.4 }}
      >
        <p className="metric-label">Decision Layer</p>
        <p className="mt-3 max-w-3xl text-xl font-medium text-white md:text-2xl">
          Not a static classifier. A reasoning-first intelligence layer that simulates analyst judgment in real time.
        </p>
      </motion.section>
    </div>
  )
}

export default LandingPage
