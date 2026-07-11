import { apiClient } from "./client";

export interface AdminBillingOverview {
  total_users: number;
  total_subscriptions: number;
  total_payment_events: number;
  unprocessed_payment_events: number;
  subscription_status_counts: Record<string, number>;
  subscription_plan_counts: Record<string, number>;
  note: string;
}

export interface AdminSubscription {
  id: string;
  user_email: string;
  plan_slug: string;
  plan_name: string;
  status: string;
  provider: string;
  provider_subscription_id: string | null;
  current_period_start: string | null;
  current_period_end: string | null;
  cancel_at_period_end: boolean;
  created_at: string;
  updated_at: string;
}

export interface AdminPaymentEvent {
  id: string;
  provider: string;
  event_type: string;
  provider_event_id: string | null;
  processed: boolean;
  processed_at: string | null;
  created_at: string;
}

export interface AdminUsageCounter {
  id: string;
  user_email: string;
  period_month: string;
  projects_used: number;
  workflow_runs_used: number;
  created_at: string;
  updated_at: string;
}

export async function getAdminBillingOverview(): Promise<AdminBillingOverview> {
  const response = await apiClient.get<AdminBillingOverview>(
    "/admin/billing/overview",
  );
  return response.data;
}

export async function getAdminSubscriptions(): Promise<AdminSubscription[]> {
  const response = await apiClient.get<AdminSubscription[]>(
    "/admin/billing/subscriptions",
  );
  return response.data;
}

export async function getAdminPaymentEvents(): Promise<AdminPaymentEvent[]> {
  const response = await apiClient.get<AdminPaymentEvent[]>(
    "/admin/billing/payment-events",
  );
  return response.data;
}

export async function getAdminUsage(): Promise<AdminUsageCounter[]> {
  const response = await apiClient.get<AdminUsageCounter[]>("/admin/billing/usage");
  return response.data;
}
