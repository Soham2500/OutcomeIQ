import { useEffect, useState } from "react";
import {
  getLaunchReadiness,
  type LaunchReadiness,
} from "../api/launchReadinessApi";
import { getApiErrorMessage } from "../api/client";
import { Badge } from "../components/Badge";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";

const readinessLabels: Array<{
  key: keyof LaunchReadiness;
  label: string;
  successWhen?: boolean;
}> = [
  { key: "debug_disabled", label: "Debug disabled", successWhen: true },
  { key: "cors_configured", label: "CORS configured", successWhen: true },
  { key: "database_configured", label: "Database configured", successWhen: true },
  {
    key: "payments_live_enabled",
    label: "Live payments enabled",
    successWhen: false,
  },
  {
    key: "razorpay_test_configured",
    label: "Razorpay test configured",
    successWhen: true,
  },
  {
    key: "policy_pages_expected",
    label: "Policy pages expected",
    successWhen: true,
  },
  {
    key: "support_email_configured",
    label: "Support email configured",
    successWhen: true,
  },
  {
    key: "admin_emails_configured",
    label: "Admin emails configured",
    successWhen: true,
  },
  {
    key: "openai_live_enabled",
    label: "OpenAI live calls enabled",
    successWhen: false,
  },
];

function statusTone(value: boolean, successWhen = true) {
  return value === successWhen ? "emerald" : "amber";
}

export function LaunchReadinessPage() {
  const [readiness, setReadiness] = useState<LaunchReadiness | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadReadiness() {
    setLoading(true);
    setError(null);
    try {
      setReadiness(await getLaunchReadiness());
    } catch (requestError) {
      setError(
        getApiErrorMessage(requestError, "Launch readiness could not be loaded."),
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadReadiness();
  }, []);

  if (loading) {
    return <LoadingState message="Loading launch readiness…" />;
  }

  if (error || !readiness) {
    return (
      <ErrorState
        message={error ?? "Launch readiness is unavailable."}
        onRetry={() => void loadReadiness()}
      />
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        description="A safe pre-launch checklist. This page reports configuration booleans only and never exposes secrets."
        title="Launch Readiness"
      />

      <SectionCard tone="brand">
        <p className="text-sm font-semibold text-brand-950">
          Environment: {readiness.app_env}
        </p>
        <p className="mt-2 text-sm leading-6 text-brand-900">{readiness.note}</p>
      </SectionCard>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {readinessLabels.map((item) => {
          const value = Boolean(readiness[item.key]);
          const desired = item.successWhen ?? true;
          return (
            <div
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-card"
              key={item.key}
            >
              <div className="flex items-center justify-between gap-3">
                <p className="font-medium text-slate-900">{item.label}</p>
                <Badge tone={statusTone(value, desired)}>
                  {value ? "true" : "false"}
                </Badge>
              </div>
              <p className="mt-2 text-xs text-slate-500">
                Expected for current safe launch: {String(desired)}
              </p>
            </div>
          );
        })}
      </section>
    </div>
  );
}
