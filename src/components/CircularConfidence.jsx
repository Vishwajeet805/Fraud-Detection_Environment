import { motion } from 'framer-motion'

function CircularConfidence({ score }) {
  const normalized = Math.max(0, Math.min(score, 100))
  const radius = 48
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (normalized / 100) * circumference

  return (
    <div className="relative flex h-28 w-28 items-center justify-center">
      <svg className="h-28 w-28 -rotate-90" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} stroke="rgba(148, 163, 184, 0.2)" strokeWidth="10" fill="none" />
        <motion.circle
          cx="60"
          cy="60"
          r={radius}
          stroke="rgba(29, 212, 191, 0.85)"
          strokeWidth="10"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.2, ease: 'easeOut' }}
        />
      </svg>
      <div className="absolute text-center">
        <p className="text-xl font-semibold text-white">{normalized}%</p>
        <p className="text-xs text-slate-400">Confidence</p>
      </div>
    </div>
  )
}

export default CircularConfidence
