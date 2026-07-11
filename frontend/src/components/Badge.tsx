import type { ReactNode } from "react";

type BadgeTone =
  | "slate"
  | "brand"
  | "emerald"
  | "amber"
  | "rose"
  | "sky"
  | "violet";

interface BadgeProps {
  children: ReactNode;
  tone?: BadgeTone;
}

const toneClasses: Record<BadgeTone, string> = {
  slate: "bg-slate-100 text-slate-700",
  brand: "bg-brand-50 text-brand-700",
  emerald: "bg-emerald-50 text-emerald-700",
  amber: "bg-amber-50 text-amber-700",
  rose: "bg-rose-50 text-rose-700",
  sky: "bg-sky-50 text-sky-700",
  violet: "bg-violet-50 text-violet-700",
};

export function Badge({ children, tone = "slate" }: BadgeProps) {
  return (
    <span
      className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold capitalize ${toneClasses[tone]}`}
    >
      {children}
    </span>
  );
}
