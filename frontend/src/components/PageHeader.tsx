import type { ReactNode } from "react";

interface PageHeaderProps {
  title: string;
  description: string;
  eyebrow?: string;
  actions?: ReactNode;
}

export function PageHeader({
  title,
  description,
  eyebrow = "OutcomeIQ",
  actions,
}: PageHeaderProps) {
  return (
    <div className="flex flex-col justify-between gap-4 rounded-3xl border border-white/60 bg-white/70 p-5 shadow-card backdrop-blur-xl lg:flex-row lg:items-end">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand-600">
          {eyebrow}
        </p>
        <h1 className="mt-1 text-3xl font-semibold tracking-tight text-slate-950 md:text-4xl">
          {title}
        </h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
          {description}
        </p>
      </div>
      {actions ? <div className="shrink-0">{actions}</div> : null}
    </div>
  );
}
