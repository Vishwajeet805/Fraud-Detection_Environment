import { NavLink } from 'react-router-dom';
import { Shield } from 'lucide-react';
import type { PropsWithChildren } from 'react';

const links = [
  ['/', 'Landing'],
  ['/detection', 'Detection'],
  ['/dashboard', 'Dashboard'],
  ['/insights', 'Training'],
  ['/how-it-works', 'How it Works'],
];

export function AppLayout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-screen bg-shell bg-radial text-slate-200">
      <header className="sticky top-0 z-40 border-b border-border/70 bg-shell/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-xl border border-border bg-panel p-2 text-accent">
              <Shield size={16} />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.18em] text-slate-400">Fraud Intelligence</p>
              <p className="text-sm font-semibold text-slate-100">Decision OS</p>
            </div>
          </div>
          <nav className="hidden gap-2 md:flex">
            {links.map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `rounded-lg px-3 py-2 text-sm transition ${isActive ? 'bg-accent/20 text-accent' : 'text-slate-400 hover:text-slate-200'}`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-10">{children}</main>
    </div>
  );
}
