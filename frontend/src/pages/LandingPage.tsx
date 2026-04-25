import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Card } from '../components/Card';
import { SectionHeader } from '../components/SectionHeader';

const features = [
  'Real-time fraud detection',
  'Sequential risk modeling',
  'Explainable AI reasoning',
  'Financial impact simulation',
];

export function LandingPage() {
  return (
    <div className="space-y-20">
      <section className="grid-shell relative overflow-hidden rounded-3xl border border-border bg-panel/40 p-12">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
          <p className="text-xs uppercase tracking-[0.2em] text-accent">Enterprise AI Risk Platform</p>
          <h1 className="mt-4 max-w-2xl text-5xl font-semibold leading-tight text-slate-100">AI Fraud Decision Intelligence</h1>
          <p className="mt-6 max-w-3xl text-lg text-slate-300">
            Multi-step fraud detection with explainable reasoning, adaptive decisions, and measurable financial protection.
          </p>
          <div className="mt-10 flex gap-4">
            <Link to="/detection" className="rounded-lg bg-accent px-5 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.02]">
              Try Live Demo
            </Link>
            <Link to="/dashboard" className="rounded-lg border border-border px-5 py-3 text-sm font-semibold text-slate-200 transition hover:border-accent/60">
              View Dashboard
            </Link>
          </div>
        </motion.div>
      </section>

      <section className="space-y-8">
        <SectionHeader
          eyebrow="Core Capabilities"
          title="Built for decision intelligence, not single-shot prediction"
        />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, idx) => (
            <motion.div key={feature} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: idx * 0.08 }}>
              <Card>
                <p className="text-base font-medium text-slate-200">{feature}</p>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
