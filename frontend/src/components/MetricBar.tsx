interface MetricBarProps {
  label: string;
  value: number;
  max?: number;
  tone?: "brand" | "emerald" | "amber" | "rose" | "slate";
  suffix?: string;
}

const toneClasses = {
  brand: "bg-brand-600",
  emerald: "bg-emerald-500",
  amber: "bg-amber-500",
  rose: "bg-rose-500",
  slate: "bg-slate-500",
};

export function MetricBar({
  label,
  value,
  max = 100,
  tone = "brand",
  suffix = "",
}: MetricBarProps) {
  const safeMax = max <= 0 ? 1 : max;
  const width = Math.max(0, Math.min(100, (value / safeMax) * 100));

  return (
    <div>
      <div className="mb-1.5 flex items-center justify-between gap-3 text-sm">
        <span className="font-medium text-slate-700">{label}</span>
        <span className="text-slate-500">
          {Number.isFinite(value) ? value.toFixed(value % 1 === 0 ? 0 : 1) : "0"}
          {suffix}
        </span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className={`h-full rounded-full ${toneClasses[tone]}`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
}
