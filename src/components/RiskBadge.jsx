const styles = {
  Safe: 'bg-emerald-400/15 text-emerald-300 border-emerald-300/30',
  Suspicious: 'bg-amber-400/15 text-amber-300 border-amber-300/30',
  Fraud: 'bg-red-400/15 text-red-300 border-red-300/30',
}

function RiskBadge({ level }) {
  return (
    <span className={`rounded-full border px-3 py-1 text-xs font-medium ${styles[level] ?? styles.Safe}`}>
      {level}
    </span>
  )
}

export default RiskBadge
