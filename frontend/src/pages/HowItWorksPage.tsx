import { BrainCircuit, DatabaseZap, ScanSearch, ShieldCheck } from 'lucide-react';
import { Card } from '../components/Card';

const steps = [
  { title: 'Step 1: Input message', icon: ScanSearch, text: 'Ingest message text, sender metadata, and URLs from user-reported activity.' },
  { title: 'Step 2: Feature extraction', icon: DatabaseZap, text: 'Compute deterministic risk signals including urgency, domain trust, and sender reputation.' },
  { title: 'Step 3: AI decision', icon: BrainCircuit, text: 'The agent performs sequential reasoning and outputs Safe, Suspicious, or Fraud with confidence.' },
  { title: 'Step 4: Reward + feedback', icon: ShieldCheck, text: 'Financial outcomes and reward signals are fed back to continuously improve policy quality.' },
];

export function HowItWorksPage() {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      {steps.map(({ title, text, icon: Icon }) => (
        <Card key={title}>
          <div className="inline-flex rounded-lg border border-border bg-shell p-2 text-accent">
            <Icon size={18} />
          </div>
          <h3 className="mt-4 text-lg font-semibold text-slate-100">{title}</h3>
          <p className="mt-2 text-sm text-slate-300">{text}</p>
        </Card>
      ))}
    </div>
  );
}
