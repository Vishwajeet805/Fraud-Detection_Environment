import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

function CircularConfidence({ score }) {
  const normalized = Math.max(0, Math.min(score, 100))
  const [displayScore, setDisplayScore] = useState(0)
  const radius = 48
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (normalized / 100) * circumference

  useEffect(() => {
    let frame
    let current = 0
    const tick = () => {
      current += Math.max(1, Math.ceil(normalized / 32))
      if (current >= normalized) {
        setDisplayScore(normalized)
        return
      }
      setDisplayScore(current)
      frame = window.setTimeout(tick, 28)
    }

    setDisplayScore(0)
    tick()

    return () => window.clearTimeout(frame)
  }, [normalized])

  return (
    <div className="relative flex h-28 w-28 items-center justify-center">
      <svg className="h-28 w-28 -rotate-90" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} stroke="rgba(148, 163, 184, 0.2)" strokeWidth="10" fill="none" />
        <motion.circle
          cx="60"
          cy="60"
          r={radius}
          stroke="rgba(41, 211, 255, 0.92)"
          strokeWidth="10"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.4, ease: 'easeOut' }}
        />
      </svg>
      <div className="absolute text-center">
        <p className="text-xl font-semibold text-white">{displayScore}%</p>
        <p className="text-xs text-slate-400">Confidence</p>
      </div>
    </div>
  )
}

export default CircularConfidence
