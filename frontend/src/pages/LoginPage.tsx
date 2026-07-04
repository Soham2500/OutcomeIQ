import { type FormEvent, useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { login } from "../api/authApi";
import { getApiErrorMessage, TOKEN_KEY } from "../api/client";

interface LoginLocationState {
  from?: string;
  registrationComplete?: boolean;
}

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LoginLocationState | null;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (localStorage.getItem(TOKEN_KEY)) {
    return <Navigate replace to="/dashboard" />;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const token = await login({ email, password });
      localStorage.setItem(TOKEN_KEY, token.access_token);
      navigate(state?.from ?? "/dashboard", { replace: true });
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Login failed."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-5 py-12">
      <section className="w-full max-w-md rounded-2xl bg-white p-7 shadow-2xl md:p-9">
        <div className="mb-7">
          <p className="text-sm font-semibold text-brand-600">OutcomeIQ</p>
          <h1 className="mt-2 text-2xl font-semibold text-slate-900">
            Welcome back
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Sign in to review workflow cost and business outcomes.
          </p>
        </div>
        {state?.registrationComplete ? (
          <p className="mb-5 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
            Registration complete. Sign in with your new account.
          </p>
        ) : null}
        {error ? (
          <p className="mb-5 rounded-lg bg-rose-50 p-3 text-sm text-rose-700">
            {error}
          </p>
        ) : null}
        <form className="space-y-5" onSubmit={handleSubmit}>
          <label>
            <span className="field-label">Email</span>
            <input
              autoComplete="email"
              className="field-input"
              onChange={(event) => setEmail(event.target.value)}
              required
              type="email"
              value={email}
            />
          </label>
          <label>
            <span className="field-label">Password</span>
            <input
              autoComplete="current-password"
              className="field-input"
              minLength={6}
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>
          <button className="primary-button w-full" disabled={submitting} type="submit">
            {submitting ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          New to OutcomeIQ?{" "}
          <Link className="font-semibold text-brand-600 hover:text-brand-700" to="/register">
            Create an account
          </Link>
        </p>
      </section>
    </main>
  );
}
