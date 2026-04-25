import { motion } from 'framer-motion';
import { Line, LineChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card } from '../components/Card';
import { rewardSeries } from '../data/mock';

export function InsightsPage() {
  return (
    <div className="space-y-6">
      <Card>
        <h2 className="text-xl font-semibold text-slate-100">Agent Learning Curve</h2>
        <div className="mt-5 h-80">
          <ResponsiveContainer>
            <LineChart data={rewardSeries}>
              <CartesianGrid stroke="#1a2940" strokeDasharray="3 3" />
              <XAxis dataKey="episode" stroke="#8ea3c2" />
              <YAxis stroke="#8ea3c2" />
              <Tooltip />
              <Line type="monotone" dataKey="baseline" stroke="#64748b" dot={false} strokeWidth={2} />
              <Line type="monotone" dataKey="improved" stroke="#2DE2B0" dot={false} strokeWidth={2.5} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <Card>
            <p className="text-sm text-slate-400">Before</p>
            <p className="mt-2 text-3xl font-semibold text-slate-100">67.2% success rate</p>
            <p className="mt-3 text-sm text-slate-300">Higher false negatives and unstable confidence under sequential pressure.</p>
          </Card>
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 12 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: 0.06 }}>
          <Card>
            <p className="text-sm text-slate-400">After</p>
            <p className="mt-2 text-3xl font-semibold text-accent">89.4% success rate</p>
            <p className="mt-3 text-sm text-slate-300">Agent improves decision-making over time with reward-guided calibration.</p>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
