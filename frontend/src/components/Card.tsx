import type { PropsWithChildren } from 'react';

export function Card({ children }: PropsWithChildren) {
  return (
    <div className="rounded-2xl border border-border/80 bg-panel/70 p-6 shadow-card backdrop-blur-xl">
      {children}
    </div>
  );
}
