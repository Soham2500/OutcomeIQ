import { type FormEvent, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { requestRegistrationOtp, verifyRegistrationOtp } from "../api/authApi";
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
    if (isApiNetworkError(requestError)) {
      setError(
        `Cannot reach backend at ${getApiBaseUrl()}. Check Amplify VITE_API_BASE_URL and backend CORS.`,
      );
    } else {
      setError(getApiErrorMessage(requestError, fallbackMessage));
    }
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
    } catch (requestError) {
      handleRequestError(requestError, "Could not resend OTP.");
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
          Verify your email with a secure OTP before your account is activated.
        </p>
        <div className="mt-5 grid grid-cols-2 rounded-xl bg-slate-100 p-1 text-center text-xs font-semibold">
          <span
            className={`rounded-lg px-3 py-2 ${
              otpRequested ? "text-slate-500" : "bg-white text-brand-700 shadow-sm"
            }`}
          >
            1. Account details
          </span>
          <span
            className={`rounded-lg px-3 py-2 ${
              otpRequested ? "bg-white text-brand-700 shadow-sm" : "text-slate-500"
            }`}
          >
            2. Email OTP
          </span>
        </div>
        {error ? (
          <p className="mt-5 rounded-lg bg-rose-50 p-3 text-sm text-rose-700">
            {error}
          </p>
        ) : null}
        {successMessage ? (
          <p className="mt-5 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
            {successMessage}
          </p>
        ) : null}
        {!otpRequested ? (
          <form className="mt-7 space-y-5" onSubmit={handleRequestOtp}>
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
              {submitting ? "Sending OTP…" : "Send verification OTP"}
            </button>
          </form>
        ) : (
          <form className="mt-7 space-y-5" onSubmit={handleVerifyOtp}>
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
              OTP sent to <span className="font-semibold text-slate-900">{email}</span>.
              Keep this page open and enter the latest 6-digit code.
            </div>
            <label>
              <span className="field-label">Email OTP</span>
              <input
                autoComplete="one-time-code"
                className="field-input text-center text-lg tracking-[0.35em]"
                inputMode="numeric"
                maxLength={6}
                minLength={6}
                onChange={(event) =>
                  setOtp(event.target.value.replace(/\D/g, "").slice(0, 6))
                }
                pattern="\d{6}"
                required
                value={otp}
              />
            </label>
            <button className="primary-button w-full" disabled={submitting} type="submit">
              {submitting ? "Verifying…" : "Verify OTP and create account"}
            </button>
            <div className="flex items-center justify-between text-sm">
              <button
                className="font-semibold text-brand-600 hover:text-brand-700 disabled:text-slate-400"
                disabled={submitting}
                onClick={handleResendOtp}
                type="button"
              >
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
          </form>
        )}
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
