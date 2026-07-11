import { Link } from "react-router-dom";

const demoSteps = [
  "Register or login with a local OutcomeIQ account.",
  "Create an organization and project from the Projects page.",
  "Run demo data from Projects, Workflows, Dashboard, or Recommendations.",
  "Open Dashboard to view workflow runs, cost, outcomes, success rate and cost per successful outcome.",
  "Open Recommendations and generate evidence-backed actions.",
  "Explain why cost per request and cost per successful outcome can lead to different decisions.",
];

export function DemoGuidePage() {
  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-2xl bg-slate-950 px-6 py-8 text-white shadow-xl md:px-10 md:py-10">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-100">
          Live MVP walkthrough
        </p>
        <h1 className="mt-3 max-w-3xl text-3xl font-semibold tracking-tight md:text-4xl">
          Prove AI workflow value using cost per successful business outcome
        </h1>
        <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-300 md:text-base">
          OutcomeIQ does not call a real AI provider in this MVP. It uses simulated
          model/tool telemetry to demonstrate the business logic: AI spend only
          matters when connected to verified outcomes.
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
            <Link className="primary-button" to="/projects">
              Create project
            </Link>
            <Link className="secondary-button" to="/dashboard">
              Open dashboard
            </Link>
            <Link className="secondary-button" to="/recommendations">
              Open recommendations
            </Link>
          </div>
        </article>

        <article className="rounded-xl border border-brand-100 bg-brand-50 p-6 shadow-card">
          <p className="text-xs font-semibold uppercase tracking-wider text-brand-700">
            Core concept
          </p>
          <blockquote className="mt-4 text-2xl font-semibold leading-snug text-slate-950">
            “The cheapest AI request is not always the cheapest successful
            outcome.”
          </blockquote>
          <p className="mt-4 text-sm leading-6 text-slate-600">
            A workflow may look cheap per request but become expensive when it
            fails, retries, falls back, or escalates. OutcomeIQ connects complete
            workflow cost with outcome evidence so teams can decide whether to
            scale, optimize, investigate, restrict, or stop.
          </p>
        </article>
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-card">
        <h2 className="text-lg font-semibold text-slate-900">What the demo uses</h2>
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border border-slate-200 p-4">
            <p className="font-semibold text-slate-900">Simulated provider</p>
            <p className="mt-2 text-sm text-slate-500">
              Model names, token counts and pricing are synthetic. No real AI API
              keys are required.
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 p-4">
            <p className="font-semibold text-slate-900">Support ticket scenario</p>
            <p className="mt-2 text-sm text-slate-500">
              The demo ticket is: “My payment failed but money was deducted.”
            </p>
          </div>
          <div className="rounded-lg border border-slate-200 p-4">
            <p className="font-semibold text-slate-900">Outcome economics</p>
            <p className="mt-2 text-sm text-slate-500">
              One run succeeds and one run fails, making failure waste and cost per
              successful outcome visible.
            </p>
          </div>
        </div>
      </section>

      <section className="rounded-xl border border-amber-200 bg-amber-50 p-6">
        <h2 className="font-semibold text-amber-950">MVP boundaries</h2>
        <ul className="mt-3 grid gap-2 text-sm text-amber-900 md:grid-cols-2">
          <li>• No real OpenAI, Anthropic, or cloud billing integration</li>
          <li>• No real provider API keys</li>
          <li>• No autonomous model routing</li>
          <li>• No production monitoring or enterprise chargeback</li>
        </ul>
      </section>
    </div>
  );
}
