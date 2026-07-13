import { type FormEvent, useState } from "react";
import { motion } from "framer-motion";
import { Eye, EyeOff, LockKeyhole, Mail, ShieldCheck, Sparkles } from "lucide-react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { login } from "../api/authApi";
import {
  getApiBaseUrl,
  getApiErrorMessage,
  isApiNetworkError,
  isApiStatus,
  TOKEN_KEY,
} from "../api/client";
import { AppLogo } from "../components/AppLogo";
import { GradientBackground } from "../components/GradientBackground";
import { useToast } from "../components/Toast";

interface LoginLocationState {
  from?: string;
  registrationComplete?: boolean;
}

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { notify } = useToast();
  const state = location.state as LoginLocationState | null;
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
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
      notify({ tone: "success", title: "Welcome back", description: "Your command center is ready." });
      navigate(state?.from ?? "/dashboard", { replace: true });
    } catch (requestError) {
      let message: string;
      if (isApiStatus(requestError, 401)) {
        message = "Invalid email or password. If using demo login, run demo seed script first.";
      } else if (isApiNetworkError(requestError)) {
        message = `Cannot reach backend at ${getApiBaseUrl()}. Check Amplify VITE_API_BASE_URL and backend CORS.`;
      } else {
        message = getApiErrorMessage(requestError, "Login failed.");
      }
      setError(message);
      notify({ tone: "error", title: "Login failed", description: message });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-5 py-10">
      <GradientBackground />
      <section className="grid w-full max-w-6xl overflow-hidden rounded-[2rem] border border-white/70 bg-white/75 shadow-2xl shadow-slate-950/15 backdrop-blur-xl lg:grid-cols-[1.05fr_0.95fr]">
        <div className="hidden bg-slate-950 p-10 text-white lg:block">
          <div className="flex h-full flex-col justify-between">
            <AppLogo inverse />
            <div>
              <motion.div
                animate={{ opacity: 1, y: 0 }}
                initial={{ opacity: 0, y: 16 }}
                transition={{ duration: 0.35 }}
              >
                <p className="inline-flex rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold text-cyan-100">
                  Outcome-aware AI FinOps
                </p>
                <h1 className="mt-5 text-4xl font-semibold tracking-tight">
                  See the real cost of successful AI outcomes.
                </h1>
                <p className="mt-4 max-w-md text-sm leading-6 text-slate-300">
                  Track tokens, retries, model spend and verified business outcomes from one premium analytics cockpit.
                </p>
              </motion.div>
              <div className="mt-8 grid gap-3">
                {[
                  "Complete workflow economics",
                  "Gemini/OpenAI usage visibility",
                  "Evidence-backed scale decisions",
                ].map((item) => (
                  <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] p-3" key={item}>
                    <ShieldCheck aria-hidden="true" className="h-5 w-5 text-emerald-300" />
                    <span className="text-sm text-slate-200">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <p className="text-xs text-slate-500">Production API: {getApiBaseUrl()}</p>
          </div>
        </div>

        <div className="p-6 md:p-10">
          <div className="lg:hidden">
            <AppLogo />
          </div>
          <div className="mt-8 max-w-md lg:mt-0">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-50 text-brand-700">
              <Sparkles aria-hidden="true" className="h-5 w-5" />
            </div>
            <h2 className="mt-5 text-3xl font-semibold tracking-tight text-slate-950">
              Welcome back
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Sign in to review AI cost, latency, tokens and outcome-level profitability.
            </p>
          </div>

          {state?.registrationComplete ? (
            <p className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
              Registration complete. Sign in with your new account.
            </p>
          ) : null}
          {error ? (
            <p className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700" role="alert">
              {error}
            </p>
          ) : null}

          <form className="mt-7 space-y-5" onSubmit={handleSubmit}>
            <label>
              <span className="field-label">Email</span>
              <div className="relative">
                <Mail aria-hidden="true" className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  autoComplete="email"
                  className="field-input pl-11"
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  type="email"
                  value={email}
                />
              </div>
            </label>
            <label>
              <span className="field-label">Password</span>
              <div className="relative">
                <LockKeyhole aria-hidden="true" className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <input
                  autoComplete="current-password"
                  className="field-input px-11"
                  minLength={6}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                  type={showPassword ? "text" : "password"}
                  value={password}
                />
                <button
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  className="absolute right-2 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
                  onClick={() => setShowPassword((current) => !current)}
                  type="button"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
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
        </div>
      </section>
    </main>
  );
}
