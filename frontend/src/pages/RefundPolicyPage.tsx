import { Link } from "react-router-dom";

export function RefundPolicyPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-5 py-10">
      <article className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-card md:p-8">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">
          OutcomeIQ policy
        </p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-950">
          Refund and Cancellation Policy
        </h1>
        <div className="mt-4 space-y-4 text-sm leading-6 text-slate-600">
          <p>
            OutcomeIQ payments are currently in test mode. Real charges are not
            enabled in this MVP, so production refunds are not processed by the
            application yet.
          </p>
          <p>
            Test subscriptions can be activated or cancelled locally for demo
            purposes. These actions do not move real money.
          </p>
          <p>
            Before commercial launch, refund windows, cancellation timing,
            invoice handling and support escalation rules must be finalized and
            legally reviewed.
          </p>
        </div>
        <Link className="secondary-button mt-8 inline-flex" to="/">
          Back to app
        </Link>
      </article>
    </main>
  );
}
