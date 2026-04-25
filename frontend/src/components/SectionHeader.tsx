interface SectionHeaderProps {
  eyebrow: string;
  title: string;
  subtitle?: string;
}

export function SectionHeader({ eyebrow, title, subtitle }: SectionHeaderProps) {
  return (
    <div className="space-y-2">
      <p className="text-xs uppercase tracking-[0.2em] text-accent">{eyebrow}</p>
      <h2 className="text-2xl font-semibold text-slate-100 md:text-3xl">{title}</h2>
      {subtitle ? <p className="max-w-2xl text-sm text-slate-400 md:text-base">{subtitle}</p> : null}
    </div>
  );
}
