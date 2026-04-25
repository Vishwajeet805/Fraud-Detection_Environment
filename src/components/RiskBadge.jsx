const styles = {
  Safe: 'bg-accent/15 text-accent border-accent/35',
  Suspicious: 'bg-warning/15 text-warning border-warning/35',
  Fraud: 'bg-danger/15 text-danger border-danger/35',
}

function RiskBadge({ level }) {
  return (
    <span className={`rounded-full border px-3 py-1 text-xs font-medium ${styles[level] ?? styles.Safe}`}>
      {level}
    </span>
  )
}

export default RiskBadge
