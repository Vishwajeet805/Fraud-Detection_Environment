import { motion } from 'framer-motion'
import SectionHeader from '../components/SectionHeader'

const steps = [
  {
    title: 'Agent',
    icon: '🤖',
    text: 'AI policy agent receives message context and prepares a decision strategy.',
  },
  {
    title: 'Action',
    icon: '⚡',
    text: 'Agent classifies the input as Safe, Suspicious, or Fraud with confidence.',
  },
  {
    title: 'Environment',
    icon: '🌐',
    text: 'Sender behavior, link intelligence, and language cues provide response context.',
  },
  {
    title: 'Reward',
    icon: '🎯',
    text: 'Correct fraud prevention receives positive reward while misses reduce policy score.',
  },
  {
    title: 'Learning',
    icon: '📈',
    text: 'Policy updates improve future decisions, reducing exposure and false positives over time.',
  },
]

function HowItWorksPage() {
  return (
    <div className="pb-8">
      <SectionHeader
        eyebrow="Workflow"
        title="How the intelligence loop works"
        description="A minimal reinforcement pipeline: Agent → Action → Environment → Reward → Learning."
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {steps.map((step, idx) => (
          <motion.article
            key={step.title}
            className="glass-card p-6"
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.3, delay: idx * 0.06 }}
            whileHover={{ y: -2, scale: 1.01 }}
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
