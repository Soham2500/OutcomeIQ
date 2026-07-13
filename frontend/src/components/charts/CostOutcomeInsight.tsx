import type { DecimalValue } from "../../types/dashboard";
import { formatLegacyCostAsINR } from "../../utils/format";

interface CostOutcomeInsightProps {
  totalCost?: DecimalValue | null;
  successfulOutcomes?: number;
  costPerSuccessfulOutcome?: DecimalValue | null;
}

export function CostOutcomeInsight({
  totalCost,
  successfulOutcomes = 0,
  costPerSuccessfulOutcome,
}: CostOutcomeInsightProps) {
  return (
    <article className="overflow-hidden rounded-xl border border-brand-100 bg-gradient-to-r from-brand-50 to-white p-6 shadow-card">
      <p className="text-xs font-semibold uppercase tracking-wider text-brand-700">
        OutcomeIQ insight
      </p>
      <h2 className="mt-2 text-xl font-semibold text-slate-900">
        Cheapest request is not always cheapest successful outcome.
      </h2>
      <p className="mt-2 max-w-3xl text-sm text-slate-600">
        Evaluate spend against verified business success before scaling an AI workflow.
      </p>
      <dl className="mt-5 grid gap-4 sm:grid-cols-3">
        <div>
          <dt className="text-xs text-slate-500">Total calculated cost</dt>
          <dd className="mt-1 font-semibold text-slate-900">{formatLegacyCostAsINR(totalCost)}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Successful outcomes</dt>
          <dd className="mt-1 font-semibold text-slate-900">{successfulOutcomes || 0}</dd>
        </div>
        <div>
          <dt className="text-xs text-slate-500">Cost per successful outcome</dt>
          <dd className="mt-1 font-semibold text-slate-900">
            {costPerSuccessfulOutcome === null || costPerSuccessfulOutcome === undefined
              ? "Not available yet"
              : formatLegacyCostAsINR(costPerSuccessfulOutcome)}
          </dd>
        </div>
      </dl>
    </article>
  );
}
