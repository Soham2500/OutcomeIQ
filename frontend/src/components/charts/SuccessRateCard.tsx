import type { DecimalValue } from "../../types/dashboard";
import { formatPercentage, toFiniteNumber } from "../../utils/formatters";

interface SuccessRateCardProps {
  successRate?: DecimalValue | null;
}

export function SuccessRateCard({ successRate }: SuccessRateCardProps) {
  const rate = toFiniteNumber(successRate);
  const progress = rate === null ? 0 : Math.min(100, Math.max(0, rate * 100));

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-card">
      <p className="text-sm font-medium text-slate-500">Success rate</p>
      <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">
        {formatPercentage(successRate)}
      </p>
      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-emerald-500 transition-all"
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="mt-2 text-xs text-slate-500">
        Share of recorded outcomes verified as successful.
      </p>
    </article>
  );
}
