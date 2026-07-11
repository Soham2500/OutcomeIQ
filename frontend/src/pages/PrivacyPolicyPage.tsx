import { Link } from "react-router-dom";

export function PrivacyPolicyPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-5 py-10">
      <article className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-card md:p-8">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">
          OutcomeIQ policy
        </p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-950">
          Privacy Policy
        </h1>
        <p className="mt-4 text-sm leading-6 text-slate-600">
          OutcomeIQ is currently an MVP and demo product. It stores account,
          project, workflow, billing-test and usage information needed to operate
          the platform. The MVP uses simulated AI provider data and should not be
          used with real customer secrets, payment card data or sensitive legal,
          health or financial records.
        </p>
        <section className="mt-6 space-y-4 text-sm leading-6 text-slate-600">
          <p>
            We do not intentionally collect real AI prompts, provider API keys or
            live payment credentials in the frontend. Backend secrets must remain
            in private environment variables only.
          </p>
          <p>
            Test payment events may be stored for debugging and launch readiness,
            but raw payment payloads are not exposed through admin UI by default.
          </p>
          <p>
            This policy page is a launch-safety placeholder for academic and MVP
            review. A lawyer-reviewed policy is required before public commercial
            launch.
          </p>
        </section>
        <Link className="secondary-button mt-8 inline-flex" to="/">
          Back to app
        </Link>
      </article>
    </main>
  );
}
