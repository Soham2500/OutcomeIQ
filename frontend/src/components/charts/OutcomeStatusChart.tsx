import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

interface OutcomeStatusChartProps {
  successful?: number;
  failed?: number;
  pending?: number;
}

export function OutcomeStatusChart({
  successful = 0,
  failed = 0,
  pending = 0,
}: OutcomeStatusChartProps) {
  const data = [
    { name: "Successful", value: Math.max(0, successful || 0), color: "#12b76a" },
    { name: "Failed", value: Math.max(0, failed || 0), color: "#f04438" },
    { name: "Pending", value: Math.max(0, pending || 0), color: "#f79009" },
  ].filter((item) => item.value > 0);

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-card">
      <h2 className="font-semibold text-slate-900">Outcome distribution</h2>
      <p className="mt-1 text-sm text-slate-500">
        Verified business outcomes across project workflow runs.
      </p>
      {data.length === 0 ? (
        <div className="flex h-64 items-center justify-center text-sm text-slate-400">
          No outcome evidence is available.
        </div>
      ) : (
        <div className="mt-3 h-64" aria-label="Workflow outcome distribution">
          <ResponsiveContainer height="100%" width="100%">
            <PieChart>
              <Pie
                cx="50%"
                cy="46%"
                data={data}
                dataKey="value"
                innerRadius={54}
                nameKey="name"
                outerRadius={82}
                paddingAngle={3}
              >
                {data.map((entry, index) => (
                  <Cell fill={entry.color} key={`${entry.name}-${index}`} />
                ))}
              </Pie>
              <Tooltip />
              <Legend iconType="circle" verticalAlign="bottom" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </article>
  );
}
