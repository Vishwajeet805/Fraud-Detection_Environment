import { motion } from 'framer-motion'

function StatCard({ label, value, trend }) {
  return (
    <motion.div
      whileHover={{ y: -2, scale: 1.01 }}
      transition={{ duration: 0.2 }}
      className="glass-card p-5"
    >
      <p className="metric-label">{label}</p>
      <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
      {trend && <p className="mt-2 text-sm text-accent">{trend}</p>}
    </motion.div>
  )
}

export default StatCard
