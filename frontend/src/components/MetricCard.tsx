import CountUp from 'react-countup';
import { motion } from 'framer-motion';
import { Card } from './Card';

interface MetricCardProps {
  label: string;
  value: number;
  suffix?: string;
}

export function MetricCard({ label, value, suffix }: MetricCardProps) {
  return (
    <motion.div whileHover={{ y: -3, scale: 1.01 }} transition={{ duration: 0.2 }}>
      <Card>
        <p className="text-sm text-slate-400">{label}</p>
        <p className="mt-3 text-3xl font-semibold text-slate-100">
          <CountUp end={value} duration={1.2} decimals={suffix === '%' ? 1 : 0} />
          {suffix}
        </p>
      </Card>
    </motion.div>
  );
}
