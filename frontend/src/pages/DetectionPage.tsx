import { motion } from 'framer-motion';
import { useMemo, useState } from 'react';
import { AlertTriangle, Globe, ShieldAlert, Siren, UserX } from 'lucide-react';
import { RadialBar, RadialBarChart, ResponsiveContainer } from 'recharts';
import { Card } from '../components/Card';
import { mockObservation, mockReward, timeline } from '../data/mock';
import { formatINR } from '../lib/api';

const scenarios = [
  'Prize claim phishing',
  'KYC suspension warning',
  'Vendor payment change',
];

export function DetectionPage() {
  const [message, setMessage] = useState(mockObservation.message_text);
  const [url, setUrl] = useState(mockObservation.url);
  const [sender, setSender] = useState(mockObservation.sender);
  const [loading, setLoading] = useState(false);

  const riskLabel = useMemo(() => {
    const score = (mockObservation.extracted_features.suspicious_domain_score + mockObservation.extracted_features.sender_reputation_score) / 2;
    if (score > 0.7) return 'Fraud';
    if (score > 0.4) return 'Suspicious';
    return 'Safe';
  }, []);

  const analyze = async () => {
    setLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 900));
    setLoading(false);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1.1fr_1fr]">
      <Card>
        <h2 className="text-xl font-semibold text-slate-100">Decision Input</h2>
        <div className="mt-6 space-y-4">
          <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={6} className="w-full rounded-xl border border-border bg-shell/80 p-4 text-sm text-slate-200 outline-none focus:border-accent/60" />
          <input value={url} onChange={(e) => setUrl(e.target.value)} className="w-full rounded-xl border border-border bg-shell/80 p-3 text-sm outline-none focus:border-accent/60" />
          <input value={sender} onChange={(e) => setSender(e.target.value)} className="w-full rounded-xl border border-border bg-shell/80 p-3 text-sm outline-none focus:border-accent/60" />
          <div className="flex flex-wrap gap-2">
            {scenarios.map((item) => (
              <button key={item} className="rounded-lg border border-border px-3 py-2 text-xs text-slate-300 transition hover:border-accent/60">
                {item}
              </button>
            ))}
          </div>
          <motion.button whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }} onClick={analyze} className="w-full rounded-xl bg-accent px-4 py-3 text-sm font-semibold text-slate-950">
            {loading ? 'Analyzing...' : 'Analyze Risk'}
          </motion.button>
        </div>
      </Card>

      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">
        <Card>
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-400">Risk Level</p>
              <p className="mt-1 text-2xl font-semibold text-slate-100">{riskLabel}</p>
            </div>
            <span className="rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs text-accent">Sequential analysis active</span>
          </div>
          <div className="mt-4 h-40">
            <ResponsiveContainer>
              <RadialBarChart innerRadius="70%" outerRadius="100%" data={[{ name: 'confidence', value: 92 }]} startAngle={180} endAngle={0}>
                <RadialBar dataKey="value" fill="#2DE2B0" cornerRadius={10} background />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
          <p className="-mt-5 text-center text-sm text-slate-300">Confidence 92%</p>
        </Card>

        <Card>
          <p className="text-sm text-slate-400">Financial Impact</p>
          <div className="mt-4 grid grid-cols-3 gap-3 text-sm">
            <div><p className="text-slate-400">₹ Saved</p><p className="text-lg font-semibold text-emerald-300">{formatINR(mockReward.money_saved)}</p></div>
            <div><p className="text-slate-400">₹ Lost</p><p className="text-lg font-semibold text-rose-300">{formatINR(mockReward.money_lost)}</p></div>
            <div><p className="text-slate-400">₹ At Risk</p><p className="text-lg font-semibold text-amber-300">{formatINR(mockReward.money_at_risk)}</p></div>
          </div>
        </Card>

        <Card>
          <p className="text-sm text-slate-400">Detected Signals</p>
          <div className="mt-4 flex flex-wrap gap-2 text-xs">
            {[
              [<AlertTriangle size={12} />, 'Urgency'],
              [<Globe size={12} />, 'External Link'],
              [<ShieldAlert size={12} />, 'Suspicious Domain'],
              [<UserX size={12} />, 'Low Reputation'],
            ].map(([icon, label]) => (
              <span key={label as string} className="inline-flex items-center gap-1 rounded-full border border-border bg-shell px-2.5 py-1.5 text-slate-300">{icon}{label}</span>
            ))}
          </div>
          <ul className="mt-4 list-disc space-y-1 pl-5 text-sm text-slate-300">
            <li>Urgency and financial intent are co-occurring in a single message.</li>
            <li>Domain and sender trust scores exceed high-risk threshold.</li>
            <li>Action confidence increased across consecutive steps.</li>
          </ul>
        </Card>

        <Card>
          <p className="text-sm text-slate-400">Decision Chain</p>
          <div className="mt-4 space-y-3">
            {timeline.map((item) => (
              <div key={item.step} className="flex items-center justify-between rounded-lg border border-border bg-shell/60 p-3 text-sm">
                <p className="flex items-center gap-2"><Siren size={14} className="text-accent" />Step {item.step} → {item.status}</p>
                <p className="text-slate-400">{Math.round(item.confidence * 100)}%</p>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>
    </div>
  );
}
