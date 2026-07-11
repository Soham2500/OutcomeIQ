interface StatCardProps {
  label: string;
  value: string | number;
  hint?: string;
  tone?: "default" | "brand" | "emerald" | "amber" | "rose";
}

const toneClasses = {
  default: "border-slate-200 bg-white",
  brand: "border-brand-100 bg-brand-50",
  emerald: "border-emerald-100 bg-emerald-50",
  amber: "border-amber-100 bg-amber-50",
  rose: "border-rose-100 bg-rose-50",
};

export function StatCard({ label, value, hint, tone = "default" }: StatCardProps) {
  return (
    <article className={`rounded-xl border p-5 shadow-card ${toneClasses[tone]}`}>
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
        {value}
      </p>
      {hint ? <p className="mt-2 text-xs text-slate-500">{hint}</p> : null}
    </article>
  );
}
