import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { DashboardWorkflowRun, DecimalValue } from "../../types/dashboard";
import { formatLegacyCostAsINR, toFiniteNumber } from "../../utils/format";

interface CostByRunChartProps {
  runs?: DashboardWorkflowRun[];
}

export function CostByRunChart({ runs = [] }: CostByRunChartProps) {
  const data = runs
    .map((run, index) => ({
      run: run.workflow_run_id?.slice(0, 6) || `Run ${index + 1}`,
      cost: toFiniteNumber(run.total_cost_usd),
    }))
    .filter((item): item is { run: string; cost: number } => item.cost !== null)
    .slice(0, 10)
    .reverse();

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-card">
      <h2 className="font-semibold text-slate-900">Cost by recent run</h2>
      <p className="mt-1 text-sm text-slate-500">
        Calculated rupee cost for the latest workflow attempts.
      </p>
      {data.length === 0 ? (
        <div className="flex h-64 items-center justify-center text-sm text-slate-400">
          No calculated run costs are available.
        </div>
      ) : (
        <div className="mt-5 h-64" aria-label="Recent workflow run costs">
          <ResponsiveContainer height="100%" width="100%">
            <BarChart data={data} margin={{ left: 4, right: 8 }}>
              <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} />
              <XAxis axisLine={false} dataKey="run" fontSize={11} tickLine={false} />
              <YAxis axisLine={false} fontSize={11} tickLine={false} width={44} />
              <Tooltip
                formatter={(value) => [formatLegacyCostAsINR(value as DecimalValue), "Cost"]}
                labelFormatter={(label) => String(label)}
              />
              <Bar dataKey="cost" fill="#6172f3" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}
