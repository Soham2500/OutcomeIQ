import { useEffect, useState } from "react";
import {
  activateTestPlan,
  createCheckout,
  getMyBilling,
  getPlans,
  type BillingPlan,
  type CheckoutResponse,
  type MyBilling,
} from "../api/billingApi";
import { getApiErrorMessage } from "../api/client";
import { Badge } from "../components/Badge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";
import { openRazorpayCheckout } from "../utils/razorpayCheckout";

function formatInr(value: BillingPlan["price_inr_monthly"]) {
  const amount = Number(value);
  if (!Number.isFinite(amount) || amount === 0) {
    return "₹0";
  }
  return `₹${amount.toLocaleString("en-IN")}`;
}

export function PricingPage() {
  const [plans, setPlans] = useState<BillingPlan[]>([]);
  const [billing, setBilling] = useState<MyBilling | null>(null);
  const [checkout, setCheckout] = useState<CheckoutResponse | null>(null);
  const [selectedPlanSlug, setSelectedPlanSlug] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [workingPlanSlug, setWorkingPlanSlug] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function loadPricing() {
    setLoading(true);
    setError(null);
    try {
      const [planData, billingData] = await Promise.all([
        getPlans(),
        getMyBilling(),
      ]);
      setPlans(planData);
      setBilling(billingData);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Pricing could not be loaded."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadPricing();
  }, []);

  async function handleCheckout(planSlug: string) {
    setWorkingPlanSlug(planSlug);
    setError(null);
    setSuccess(null);
    try {
      const response = await createCheckout(planSlug);
      setCheckout(response);
      setSelectedPlanSlug(planSlug);
      if (response.checkout_type === "razorpay_subscription") {
        await openRazorpayCheckout(
          response,
          (message) => {
            setSuccess(message);
          },
          (message) => {
            setError(message);
          },
        );
      }
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Test checkout could not be created."));
    } finally {
      setWorkingPlanSlug(null);
    }
  }

  async function handleActivate(planSlug: string) {
    setWorkingPlanSlug(planSlug);
    setError(null);
    setSuccess(null);
    try {
      await activateTestPlan(planSlug);
      setSuccess("Test plan activated. No real payment was charged.");
      setCheckout(null);
      setSelectedPlanSlug(null);
      await loadPricing();
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Test plan could not be activated."));
    } finally {
      setWorkingPlanSlug(null);
    }
  }

  if (loading) {
    return <LoadingState message="Loading plans…" />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        description="Subscription-ready plan structure for launch preparation. Payments are currently test/sandbox only."
        title="Pricing"
      />

      <SectionCard tone="brand">
        <p className="text-sm font-semibold text-brand-950">
          Payments are currently in test mode for MVP launch preparation.
        </p>
        <p className="mt-2 text-sm leading-6 text-brand-900">
          No real Razorpay or Stripe charge is made from this page. Real payments
          require KYC, policies, webhook verification and production checks.
        </p>
      </SectionCard>

      {error ? <ErrorState message={error} onRetry={() => void loadPricing()} /> : null}
      {success ? (
        <p className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
          {success}
        </p>
      ) : null}

      {plans.length === 0 ? (
        <EmptyState
          description="Run the billing migration and seed plans before using pricing."
          title="No plans available"
        />
      ) : (
        <section className="grid gap-5 lg:grid-cols-3">
          {plans.map((plan) => {
            const current = billing?.plan.slug === plan.slug;
            const paid = Number(plan.price_inr_monthly) > 0;
            return (
              <article
                className={`rounded-2xl border bg-white p-6 shadow-card ${
                  current ? "border-brand-300 ring-2 ring-brand-100" : "border-slate-200"
                }`}
                key={plan.id}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-xl font-semibold text-slate-900">
                      {plan.name}
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">
                      {plan.description}
                    </p>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    {plan.slug === "free" ? <Badge tone="slate">Free</Badge> : null}
                    {plan.slug === "starter" ? (
                      <Badge tone="brand">Recommended</Badge>
                    ) : null}
                    {paid ? <Badge tone="amber">Test Mode</Badge> : null}
                    {current ? <Badge tone="emerald">Current</Badge> : null}
                  </div>
                </div>
                <p className="mt-6 text-3xl font-semibold text-slate-950">
                  {formatInr(plan.price_inr_monthly)}
                  <span className="text-sm font-medium text-slate-500">/month</span>
                </p>
                <ul className="mt-6 space-y-2 text-sm text-slate-600">
                  <li>• {plan.max_projects} project(s)</li>
                  <li>• {plan.max_workflow_runs_per_month} workflow runs/month</li>
                  <li>• {plan.max_team_members} team member(s)</li>
                  <li>• Analytics: {plan.analytics_enabled ? "included" : "disabled"}</li>
                  <li>• Export: {plan.export_enabled ? "included" : "disabled"}</li>
                  <li>
                    • Recommendations:{" "}
                    {plan.recommendations_enabled ? "included" : "disabled"}
                  </li>
                  <li>
                    • Real AI provider:{" "}
                    {plan.openai_provider_enabled ? "future flag" : "not enabled"}
                  </li>
                </ul>
                <button
                  className={current ? "secondary-button mt-6 w-full" : "primary-button mt-6 w-full"}
                  disabled={current || workingPlanSlug === plan.slug}
                  onClick={() =>
                    paid
                      ? void handleCheckout(plan.slug)
                      : void handleActivate(plan.slug)
                  }
                  type="button"
                >
                  {current
                    ? "Current Plan"
                    : workingPlanSlug === plan.slug
                      ? "Preparing…"
                      : paid
                        ? "Start Razorpay Test Checkout"
                        : "Start Free"}
                </button>
              </article>
            );
          })}
        </section>
      )}

      {checkout && selectedPlanSlug ? (
        <SectionCard
          title="Test checkout prepared"
          description={checkout.message}
          actions={
            <button
              className="primary-button"
              disabled={workingPlanSlug === selectedPlanSlug}
              onClick={() => void handleActivate(selectedPlanSlug)}
              type="button"
            >
              Activate Test Plan Locally
            </button>
          }
        >
          <div className="space-y-2 text-sm text-slate-600">
            <p>Provider: {checkout.provider}</p>
            <p>Mode: {checkout.mode}</p>
            <p>Plan: {checkout.plan_slug}</p>
            <p>Checkout type: {checkout.checkout_type}</p>
            {checkout.subscription_id ? (
              <p>Test subscription: {checkout.subscription_id}</p>
            ) : null}
            {checkout.test_checkout_url ? <p>Test URL: {checkout.test_checkout_url}</p> : null}
            <p className="text-xs text-slate-400">
              Real payments are not enabled. This checkout is for test/sandbox validation.
            </p>
          </div>
        </SectionCard>
      ) : null}
    </div>
  );
}
