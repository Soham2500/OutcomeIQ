import { Link } from "react-router-dom";

export function TermsPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-5 py-10">
      <article className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-card md:p-8">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">
          OutcomeIQ policy
        </p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-950">
          Terms of Use
        </h1>
        <div className="mt-4 space-y-4 text-sm leading-6 text-slate-600">
          <p>
            OutcomeIQ is provided as an MVP for education, demonstration and
            launch validation. It helps teams inspect AI workflow cost, outcomes,
            failure waste and test-mode billing readiness.
          </p>
          <p>
            The platform must not be treated as financial, legal or compliance
            advice. Recommendations are evidence-backed product signals, not
            autonomous business decisions.
          </p>
          <p>
            Real payments and real AI provider calls are disabled until launch
            approval, production controls and policy review are complete.
          </p>
          <p>
            These terms are a practical MVP placeholder. Commercial launch
            requires formal legal review.
          </p>
        </div>
        <Link className="secondary-button mt-8 inline-flex" to="/">
          Back to app
        </Link>
      </article>
    </main>
  );
}
