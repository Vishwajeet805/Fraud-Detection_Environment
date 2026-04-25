import { motion } from 'framer-motion'

function SectionHeader({ eyebrow, title, description }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ duration: 0.4 }}
      className="mb-8"
    >
      {eyebrow && <p className="mb-2 text-xs uppercase tracking-[0.22em] text-accent/90">{eyebrow}</p>}
      <h2 className="text-2xl font-semibold text-white md:text-3xl">{title}</h2>
      {description && <p className="mt-2 max-w-2xl text-sm text-slate-300 md:text-base">{description}</p>}
    </motion.div>
  )
}

export default SectionHeader
