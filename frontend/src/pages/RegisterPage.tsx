import { type FormEvent, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { register } from "../api/authApi";
import {
  getApiBaseUrl,
  getApiErrorMessage,
  isApiNetworkError,
  TOKEN_KEY,
} from "../api/client";
import { AppLogo } from "../components/AppLogo";

export function RegisterPage() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
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
      await register({ full_name: fullName, email, password });
      navigate("/login", {
        replace: true,
        state: { registrationComplete: true },
      });
    } catch (requestError) {
      if (isApiNetworkError(requestError)) {
        setError(
          `Cannot reach backend at ${getApiBaseUrl()}. Check Amplify VITE_API_BASE_URL and backend CORS.`,
        );
      } else {
        setError(getApiErrorMessage(requestError, "Registration failed."));
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-5 py-12">
      <section className="w-full max-w-md rounded-2xl bg-white p-7 shadow-2xl md:p-9">
        <AppLogo />
        <h1 className="mt-2 text-2xl font-semibold text-slate-900">
          Create your account
        </h1>
        <p className="mt-2 text-sm text-slate-500">
          Start with synthetic workflow evidence and outcome-aware economics.
        </p>
        {error ? (
          <p className="mt-5 rounded-lg bg-rose-50 p-3 text-sm text-rose-700">
            {error}
          </p>
        ) : null}
        <form className="mt-7 space-y-5" onSubmit={handleSubmit}>
          <label>
            <span className="field-label">Full name</span>
            <input
              autoComplete="name"
              className="field-input"
              onChange={(event) => setFullName(event.target.value)}
              required
              value={fullName}
            />
          </label>
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
              autoComplete="new-password"
              className="field-input"
              minLength={6}
              onChange={(event) => setPassword(event.target.value)}
              required
              type="password"
              value={password}
            />
          </label>
          <button className="primary-button w-full" disabled={submitting} type="submit">
            {submitting ? "Creating account…" : "Create account"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-500">
          Already registered?{" "}
          <Link className="font-semibold text-brand-600 hover:text-brand-700" to="/login">
            Sign in
          </Link>
        </p>
      </section>
    </main>
  );
}
