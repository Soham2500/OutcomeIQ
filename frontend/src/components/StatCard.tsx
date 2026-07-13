interface StatCardProps {
  label: string;
  value: string | number;
  hint?: string;
  tone?: "default" | "brand" | "emerald" | "amber" | "rose";
}

const toneClasses = {
  default: "border-white/70 bg-white/80",
  brand: "border-brand-200 bg-gradient-to-br from-brand-50 to-cyan-50",
  emerald: "border-emerald-200 bg-gradient-to-br from-emerald-50 to-teal-50",
  amber: "border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50",
  rose: "border-rose-200 bg-gradient-to-br from-rose-50 to-pink-50",
};

export function StatCard({ label, value, hint, tone = "default" }: StatCardProps) {
  return (
    <article className={`rounded-3xl border p-5 shadow-card backdrop-blur transition duration-200 hover:-translate-y-1 hover:shadow-soft ${toneClasses[tone]}`}>
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-950 tabular-nums">
        {value}
      </p>
      {hint ? <p className="mt-2 text-xs text-slate-500">{hint}</p> : null}
    </article>
  );
}
