import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  cancelSubscription,
  getMyBilling,
  type MyBilling,
} from "../api/billingApi";
import { getApiErrorMessage } from "../api/client";
import { Badge } from "../components/Badge";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { MetricBar } from "../components/MetricBar";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";
import { StatCard } from "../components/StatCard";

export function BillingPage() {
  const [billing, setBilling] = useState<MyBilling | null>(null);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function loadBilling() {
    setLoading(true);
    setError(null);
    try {
      setBilling(await getMyBilling());
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Billing could not be loaded."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadBilling();
  }, []);

  async function handleCancel() {
    setCancelling(true);
    setError(null);
    setSuccess(null);
    try {
      await cancelSubscription();
      setSuccess("Subscription cancelled in local/test mode.");
      await loadBilling();
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Subscription could not be cancelled."));
    } finally {
      setCancelling(false);
    }
  }

  if (loading) {
    return <LoadingState message="Loading billing…" />;
  }

  if (!billing) {
    return <ErrorState message={error ?? "Billing information is unavailable."} />;
  }

  const onFreePlan = billing.plan.slug === "free";

  return (
    <div className="space-y-6">
      <PageHeader
        description="Current subscription, monthly usage and test-mode billing status."
        title="Billing"
        actions={
          <Link className="primary-button" to="/pricing">
            Upgrade from Pricing
          </Link>
        }
      />

      {error ? <ErrorState message={error} onRetry={() => void loadBilling()} /> : null}
      {success ? (
        <p className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
          {success}
        </p>
      ) : null}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Current plan" value={billing.plan.name} />
        <StatCard label="Subscription status" value={billing.subscription.status} />
        <StatCard label="Payment mode" value={billing.payment_mode} />
        <StatCard label="Provider" value={billing.subscription.provider} />
      </section>

      {billing.subscription.provider_subscription_id ? (
        <SectionCard title="Provider reference">
          <p className="font-mono text-sm text-slate-700">
            {billing.subscription.provider_subscription_id}
          </p>
          <p className="mt-2 text-xs text-slate-500">
            This is a safe test-mode subscription reference. No secret keys are shown.
          </p>
        </SectionCard>
      ) : null}

      <SectionCard tone="brand">
        <p className="text-sm font-semibold text-brand-950">
          Payments are in test mode. Real payment mode is not enabled yet.
        </p>
        <p className="mt-2 text-sm leading-6 text-brand-900">
          Backend webhooks control subscription confirmation. The frontend never
          stores Razorpay secrets and does not directly mark payments successful.
        </p>
      </SectionCard>

      <SectionCard
        title="Monthly usage"
        description={`Usage period: ${billing.usage.period_month}`}
      >
        <div className="space-y-5">
          <MetricBar
            label="Projects used"
            max={billing.usage.max_projects}
            value={billing.usage.projects_used}
          />
          <MetricBar
            label="Workflow runs used"
            max={billing.usage.max_workflow_runs_per_month}
            value={billing.usage.workflow_runs_used}
          />
        </div>
      </SectionCard>

      <SectionCard title="Subscription actions">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
          <div>
            {onFreePlan ? (
              <p className="text-sm text-slate-600">
                You are on the Free plan. Upgrade in test mode when you need more
                projects or workflow runs.
              </p>
            ) : (
              <p className="text-sm text-slate-600">
                This is a test/sandbox subscription. No real payment has been charged.
              </p>
            )}
            <div className="mt-3 flex flex-wrap gap-2">
              <Badge tone={onFreePlan ? "slate" : "emerald"}>
                {billing.plan.slug}
              </Badge>
              <Badge tone="brand">{billing.payment_mode}</Badge>
            </div>
          </div>
          {!onFreePlan ? (
            <button
              className="secondary-button"
              disabled={cancelling}
              onClick={() => void handleCancel()}
              type="button"
            >
              {cancelling ? "Cancelling…" : "Cancel test subscription"}
            </button>
          ) : null}
        </div>
      </SectionCard>
    </div>
  );
}
