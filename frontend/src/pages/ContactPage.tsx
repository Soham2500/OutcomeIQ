import { Link } from "react-router-dom";

export function ContactPage() {
  return (
    <main className="min-h-screen bg-slate-50 px-5 py-10">
      <article className="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-card md:p-8">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">
          OutcomeIQ support
        </p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-950">Contact</h1>
        <p className="mt-4 text-sm leading-6 text-slate-600">
          For MVP review, deployment questions, billing-test issues or project
          evaluation, contact the OutcomeIQ maintainer. Configure the production
          support email through the backend SUPPORT_EMAIL environment variable
          before a public launch.
        </p>
        <div className="mt-6 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
          <p className="font-semibold text-slate-900">Support status</p>
          <p className="mt-1">
            This page is intentionally static. No contact form data is collected
            by the frontend in the MVP.
          </p>
        </div>
        <Link className="secondary-button mt-8 inline-flex" to="/">
          Back to app
        </Link>
      </article>
    </main>
  );
}
