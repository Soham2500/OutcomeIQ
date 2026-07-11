import { useEffect, useState } from "react";
import {
  getAdminBillingOverview,
  getAdminPaymentEvents,
  getAdminSubscriptions,
  getAdminUsage,
  type AdminBillingOverview,
  type AdminPaymentEvent,
  type AdminSubscription,
  type AdminUsageCounter,
} from "../api/adminBillingApi";
import { getApiErrorMessage, isApiStatus } from "../api/client";
import { Badge } from "../components/Badge";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";
import { StatCard } from "../components/StatCard";

export function AdminBillingPage() {
  const [overview, setOverview] = useState<AdminBillingOverview | null>(null);
  const [subscriptions, setSubscriptions] = useState<AdminSubscription[]>([]);
  const [events, setEvents] = useState<AdminPaymentEvent[]>([]);
  const [usage, setUsage] = useState<AdminUsageCounter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadAdminBilling() {
    setLoading(true);
    setError(null);
    try {
      const [overviewData, subscriptionData, eventData, usageData] =
        await Promise.all([
          getAdminBillingOverview(),
          getAdminSubscriptions(),
          getAdminPaymentEvents(),
          getAdminUsage(),
        ]);
      setOverview(overviewData);
      setSubscriptions(subscriptionData);
      setEvents(eventData);
      setUsage(usageData);
    } catch (requestError) {
      if (isApiStatus(requestError, 403)) {
        setError("Admin billing access is restricted for this account.");
      } else {
        setError(
          getApiErrorMessage(requestError, "Admin billing could not be loaded."),
        );
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadAdminBilling();
  }, []);

  if (loading) {
    return <LoadingState message="Loading admin billing…" />;
  }

  if (error) {
    return <ErrorState message={error} onRetry={() => void loadAdminBilling()} />;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        description="Read-only launch-safety billing inspection. Raw payment payloads and provider secrets are never shown."
        title="Admin Billing"
      />

      {overview ? (
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard label="Users" value={overview.total_users} />
          <StatCard label="Subscriptions" value={overview.total_subscriptions} />
          <StatCard label="Payment events" value={overview.total_payment_events} />
          <StatCard
            label="Unprocessed events"
            value={overview.unprocessed_payment_events}
          />
        </section>
      ) : null}

      <SectionCard title="Subscriptions" description="Provider IDs are masked.">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500">
              <tr>
                <th className="px-3 py-2">User</th>
                <th className="px-3 py-2">Plan</th>
                <th className="px-3 py-2">Status</th>
                <th className="px-3 py-2">Provider</th>
                <th className="px-3 py-2">Reference</th>
              </tr>
            </thead>
            <tbody>
              {subscriptions.map((subscription) => (
                <tr className="border-t border-slate-100" key={subscription.id}>
                  <td className="px-3 py-3">{subscription.user_email}</td>
                  <td className="px-3 py-3">{subscription.plan_name}</td>
                  <td className="px-3 py-3">
                    <Badge tone="brand">{subscription.status}</Badge>
                  </td>
                  <td className="px-3 py-3">{subscription.provider}</td>
                  <td className="px-3 py-3 font-mono text-xs">
                    {subscription.provider_subscription_id ?? "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {subscriptions.length === 0 ? (
            <p className="py-4 text-sm text-slate-500">No subscriptions found.</p>
          ) : null}
        </div>
      </SectionCard>

      <section className="grid gap-6 xl:grid-cols-2">
        <SectionCard title="Payment events" description="Raw payloads are hidden.">
          <div className="space-y-3">
            {events.map((event) => (
              <div className="rounded-lg border border-slate-100 p-3" key={event.id}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium text-slate-900">{event.event_type}</p>
                  <Badge tone={event.processed ? "emerald" : "amber"}>
                    {event.processed ? "processed" : "stored"}
                  </Badge>
                </div>
                <p className="mt-1 text-xs text-slate-500">
                  {event.provider} · {event.provider_event_id ?? "no event id"}
                </p>
              </div>
            ))}
            {events.length === 0 ? (
              <p className="text-sm text-slate-500">No payment events found.</p>
            ) : null}
          </div>
        </SectionCard>

        <SectionCard title="Usage counters">
          <div className="space-y-3">
            {usage.map((counter) => (
              <div className="rounded-lg border border-slate-100 p-3" key={counter.id}>
                <p className="font-medium text-slate-900">{counter.user_email}</p>
                <p className="mt-1 text-sm text-slate-600">
                  {counter.period_month}: {counter.projects_used} project(s),{" "}
                  {counter.workflow_runs_used} workflow run(s)
                </p>
              </div>
            ))}
            {usage.length === 0 ? (
              <p className="text-sm text-slate-500">No usage counters found.</p>
            ) : null}
          </div>
        </SectionCard>
      </section>
    </div>
  );
}
