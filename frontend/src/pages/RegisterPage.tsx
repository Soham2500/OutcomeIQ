import { type FormEvent, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Eye, EyeOff, LockKeyhole, Mail, ShieldCheck, UserRound } from "lucide-react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { requestRegistrationOtp, verifyRegistrationOtp } from "../api/authApi";
import {
  getApiBaseUrl,
  getApiErrorMessage,
  isApiNetworkError,
  TOKEN_KEY,
} from "../api/client";
import { AppLogo } from "../components/AppLogo";
import { GradientBackground } from "../components/GradientBackground";
import { useToast } from "../components/Toast";

export function RegisterPage() {
  const navigate = useNavigate();
  const { notify } = useToast();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [otp, setOtp] = useState("");
  const [otpRequested, setOtpRequested] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (localStorage.getItem(TOKEN_KEY)) {
    return <Navigate replace to="/dashboard" />;
  }

  function getRegistrationPayload() {
    return { full_name: fullName, email, password };
  }

  function handleRequestError(requestError: unknown, fallbackMessage: string) {
    const message = isApiNetworkError(requestError)
      ? `Cannot reach backend at ${getApiBaseUrl()}. Check Amplify VITE_API_BASE_URL and backend CORS.`
      : getApiErrorMessage(requestError, fallbackMessage);
    setError(message);
    notify({ tone: "error", title: fallbackMessage, description: message });
  }

  async function handleRequestOtp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccessMessage(null);
    try {
      await requestRegistrationOtp(getRegistrationPayload());
      setOtpRequested(true);
      setOtp("");
      setSuccessMessage("OTP sent to your email. It expires in 10 minutes.");
      notify({ tone: "success", title: "OTP sent", description: "Check your Gmail inbox for the latest code." });
    } catch (requestError) {
      handleRequestError(requestError, "Could not send OTP.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleVerifyOtp(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccessMessage(null);
    try {
      await verifyRegistrationOtp({ email, otp });
      notify({ tone: "success", title: "Account verified", description: "Sign in to enter OutcomeIQ." });
      navigate("/login", {
        replace: true,
        state: { registrationComplete: true },
      });
    } catch (requestError) {
      handleRequestError(requestError, "OTP verification failed.");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleResendOtp() {
    setSubmitting(true);
    setError(null);
    setSuccessMessage(null);
    try {
      await requestRegistrationOtp(getRegistrationPayload());
      setOtp("");
      setSuccessMessage("A fresh OTP has been sent. Please use the latest code.");
      notify({ tone: "success", title: "Fresh OTP sent" });
    } catch (requestError) {
      handleRequestError(requestError, "Could not resend OTP.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-5 py-10">
      <GradientBackground />
      <section className="grid w-full max-w-6xl overflow-hidden rounded-[2rem] border border-white/70 bg-white/75 shadow-2xl shadow-slate-950/15 backdrop-blur-xl lg:grid-cols-[0.95fr_1.05fr]">
        <div className="p-6 md:p-10">
          <AppLogo />
          <div className="mt-8 max-w-lg">
            <h1 className="text-3xl font-semibold tracking-tight text-slate-950">
              Create your OutcomeIQ workspace
            </h1>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              Verify your email with OTP before account activation. No provider keys ever touch the browser.
            </p>
          </div>

          <div className="mt-6 grid grid-cols-2 rounded-2xl bg-slate-100 p-1 text-center text-xs font-semibold">
            <span className={`rounded-xl px-3 py-2 transition ${otpRequested ? "text-slate-500" : "bg-white text-brand-700 shadow-sm"}`}>
              1. Account details
            </span>
            <span className={`rounded-xl px-3 py-2 transition ${otpRequested ? "bg-white text-brand-700 shadow-sm" : "text-slate-500"}`}>
              2. Email OTP
            </span>
          </div>

          {error ? (
            <p className="mt-5 rounded-2xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700" role="alert">
              {error}
            </p>
          ) : null}
          {successMessage ? (
            <p className="mt-5 rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
              {successMessage}
            </p>
          ) : null}

          <AnimatePresence mode="wait">
            {!otpRequested ? (
              <motion.form
                animate={{ opacity: 1, x: 0 }}
                className="mt-7 space-y-5"
                exit={{ opacity: 0, x: -12 }}
                initial={{ opacity: 0, x: 12 }}
                key="details"
                onSubmit={handleRequestOtp}
              >
                <label>
                  <span className="field-label">Full name</span>
                  <div className="relative">
                    <UserRound aria-hidden="true" className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                    <input
                      autoComplete="name"
                      className="field-input pl-11"
                      onChange={(event) => setFullName(event.target.value)}
                      required
                      value={fullName}
                    />
                  </div>
                </label>
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
                      autoComplete="new-password"
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
                  {submitting ? "Sending OTP…" : "Send verification OTP"}
                </button>
              </motion.form>
            ) : (
              <motion.form
                animate={{ opacity: 1, x: 0 }}
                className="mt-7 space-y-5"
                exit={{ opacity: 0, x: 12 }}
                initial={{ opacity: 0, x: -12 }}
                key="otp"
                onSubmit={handleVerifyOtp}
              >
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                  OTP sent to <span className="font-semibold text-slate-900">{email}</span>. Enter the latest 6-digit code.
                </div>
                <label>
                  <span className="field-label">Email OTP</span>
                  <input
                    autoComplete="one-time-code"
                    className="field-input text-center font-mono text-xl tracking-[0.45em]"
                    inputMode="numeric"
                    maxLength={6}
                    minLength={6}
                    onChange={(event) => setOtp(event.target.value.replace(/\D/g, "").slice(0, 6))}
                    pattern="\d{6}"
                    required
                    value={otp}
                  />
                </label>
                <button className="primary-button w-full" disabled={submitting} type="submit">
                  {submitting ? "Verifying…" : "Verify OTP and create account"}
                </button>
                <div className="flex items-center justify-between text-sm">
                  <button className="font-semibold text-brand-600 hover:text-brand-700 disabled:text-slate-400" disabled={submitting} onClick={handleResendOtp} type="button">
                    Resend OTP
                  </button>
                  <button
                    className="font-semibold text-slate-500 hover:text-slate-700 disabled:text-slate-400"
                    disabled={submitting}
                    onClick={() => {
                      setOtpRequested(false);
                      setOtp("");
                      setError(null);
                      setSuccessMessage(null);
                    }}
                    type="button"
                  >
                    Edit details
                  </button>
                </div>
              </motion.form>
            )}
          </AnimatePresence>

          <p className="mt-6 text-center text-sm text-slate-500">
            Already registered?{" "}
            <Link className="font-semibold text-brand-600 hover:text-brand-700" to="/login">
              Sign in
            </Link>
          </p>
        </div>

        <div className="hidden bg-slate-950 p-10 text-white lg:block">
          <div className="flex h-full flex-col justify-between">
            <div className="rounded-3xl border border-white/10 bg-white/[0.06] p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
                Secure SaaS onboarding
              </p>
              <h2 className="mt-4 text-3xl font-semibold tracking-tight">
                Outcome contracts, verified economics, AI cost evidence.
              </h2>
            </div>
            <div className="grid gap-3">
              {["Gmail OTP verification", "Backend-only AI provider keys", "Outcome-aware dashboards"].map((item) => (
                <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] p-3" key={item}>
                  <ShieldCheck aria-hidden="true" className="h-5 w-5 text-emerald-300" />
                  <span className="text-sm text-slate-200">{item}</span>
                </div>
              ))}
            </div>
            <p className="text-xs text-slate-500">Registration API: {getApiBaseUrl()}</p>
          </div>
        </div>
      </section>
    </main>
  );
}
