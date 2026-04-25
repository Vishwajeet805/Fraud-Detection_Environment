import { motion } from 'framer-motion'
import SectionHeader from '../components/SectionHeader'

const steps = [
  {
    title: 'Step 1: Input message',
    icon: '✉️',
    text: 'Ingest message text, sender identity, and destination URL from the transaction context.',
  },
  {
    title: 'Step 2: Feature extraction',
    icon: '🧠',
    text: 'Generate structured risk features from language intent, link intelligence, and reputation signals.',
  },
  {
    title: 'Step 3: AI decision',
    icon: '🛡️',
    text: 'Run sequential policy logic to classify risk as Safe, Suspicious, or Fraud with calibrated confidence.',
  },
  {
    title: 'Step 4: Reward + feedback',
    icon: '📈',
    text: 'Feed outcomes into the reward loop to continuously improve risk containment and decision quality.',
  },
]

function HowItWorksPage() {
  return (
    <div className="pb-8">
      <SectionHeader
        eyebrow="Workflow"
        title="How the platform makes resilient fraud decisions"
        description="A minimal four-step architecture designed for explainable, measurable, and continuously improving fraud defense."
      />

      <div className="grid gap-4 md:grid-cols-2">
        {steps.map((step, idx) => (
          <motion.article
            key={step.title}
            className="glass-card p-6"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.3, delay: idx * 0.07 }}
            whileHover={{ y: -2 }}
          >
            <div className="flex items-center gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-lg">
                {step.icon}
              </span>
              <h3 className="text-lg font-semibold text-white">{step.title}</h3>
            </div>
            <p className="mt-3 text-sm text-slate-300">{step.text}</p>
          </motion.article>
        ))}
      </div>
    </div>
  )
}

export default HowItWorksPage
