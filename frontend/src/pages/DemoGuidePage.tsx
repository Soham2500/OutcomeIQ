import { Link } from "react-router-dom";

const demoSteps = [
  "Login with the local demo account",
  "Select the AI Support Cost Optimization Demo project",
  "Review five simulated workflow runs",
  "View the total workflow cost",
  "Inspect successful, failed and escalated outcomes",
  "Read cost per successful outcome",
  "Generate and review rule-based recommendations",
];

const setupCommands = [
  {
    label: "Backend",
    command:
      "cd C:\\Users\\soham\\OneDrive\\Documents\\pro\n.\\scripts\\run_backend.ps1",
  },
  {
    label: "Seed demo data",
    command: ".\\scripts\\seed_demo_data_via_api.ps1",
  },
  {
    label: "Frontend",
    command: ".\\scripts\\run_frontend.ps1",
  },
];

export function DemoGuidePage() {
  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-2xl bg-slate-950 px-6 py-8 text-white shadow-xl md:px-10 md:py-10">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-100">
          Evaluator walkthrough
        </p>
        <h1 className="mt-3 max-w-3xl text-3xl font-semibold tracking-tight md:text-4xl">
          From AI workflow spend to verified business value
        </h1>
        <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-300 md:text-base">
          Companies can track tokens, model calls and cloud cost, but often cannot
          answer what an AI workflow cost per successful business outcome. OutcomeIQ
          connects those two sides of the decision.
        </p>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-card">
          <p className="text-xs font-semibold uppercase tracking-wider text-brand-600">
            Demo flow
          </p>
          <ol className="mt-5 space-y-3">
            {demoSteps.map((step, index) => (
              <li className="flex items-start gap-3" key={step}>
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-brand-50 text-xs font-semibold text-brand-700">
                  {index + 1}
                </span>
                <span className="pt-1 text-sm text-slate-700">{step}</span>
              </li>
            ))}
          </ol>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link className="primary-button" to="/dashboard">
              Start with dashboard
            </Link>
            <Link className="secondary-button" to="/recommendations">
              Open recommendations
            </Link>
          </div>
        </article>

        <article className="rounded-xl border border-brand-100 bg-brand-50 p-6 shadow-card">
          <p className="text-xs font-semibold uppercase tracking-wider text-brand-700">
            Core proof
          </p>
          <blockquote className="mt-4 text-2xl font-semibold leading-snug text-slate-950">
            “Cheapest AI request is not always cheapest successful outcome.”
          </blockquote>
          <p className="mt-4 text-sm leading-6 text-slate-600">
            A low-cost workflow can become expensive when failures, retries and
            escalations reduce successful yield. OutcomeIQ makes that unit economics
            visible before a company scales the workflow.
          </p>
        </article>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-card">
        <h2 className="text-lg font-semibold text-slate-900">Local demo setup</h2>
        <p className="mt-1 text-sm text-slate-500">
          Run each service from the project root in its own PowerShell window.
        </p>
        <div className="mt-5 grid gap-4 lg:grid-cols-3">
          {setupCommands.map((item) => (
            <div
              className="overflow-hidden rounded-lg border border-slate-200"
              key={item.label}
            >
              <p className="border-b border-slate-200 bg-slate-50 px-4 py-2 text-xs font-semibold text-slate-600">
                {item.label}
              </p>
              <pre className="min-h-24 overflow-x-auto bg-slate-950 p-4 text-xs leading-5 text-slate-200">
                <code>{item.command}</code>
              </pre>
            </div>
          ))}
        </div>
        <div className="mt-5 rounded-lg border border-emerald-200 bg-emerald-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-wider text-emerald-700">
            Demo login
          </p>
          <p className="mt-2 font-mono text-sm text-emerald-950">
            demo@outcomeiq.local / Demo@12345
          </p>
        </div>
      </section>

      <section className="rounded-xl border border-amber-200 bg-amber-50 p-6">
        <h2 className="font-semibold text-amber-950">What is simulated</h2>
        <ul className="mt-3 grid gap-2 text-sm text-amber-900 md:grid-cols-2">
          <li>• AI model calls and tool telemetry</li>
          <li>• Local non-production pricing rates</li>
          <li>• Customer-support outcomes and evidence</li>
          <li>• No real provider billing or API keys</li>
        </ul>
      </section>
    </div>
  );
}
