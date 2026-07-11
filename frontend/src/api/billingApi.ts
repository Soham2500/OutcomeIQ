import { apiClient } from "./client";
import type { DecimalValue } from "../types/dashboard";

export interface BillingPlan {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  price_inr_monthly: DecimalValue;
  currency: string;
  max_projects: number;
  max_workflow_runs_per_month: number;
  max_team_members: number;
  export_enabled: boolean;
  analytics_enabled: boolean;
  recommendations_enabled: boolean;
  openai_provider_enabled: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BillingSubscription {
  id: string;
  user_id: string;
  plan_id: string;
  status: string;
  provider: string;
  provider_subscription_id: string | null;
  current_period_start: string | null;
  current_period_end: string | null;
  cancel_at_period_end: boolean;
  created_at: string;
  updated_at: string;
}

export interface BillingUsage {
  period_month: string;
  projects_used: number;
  max_projects: number;
  workflow_runs_used: number;
  max_workflow_runs_per_month: number;
}

export interface MyBilling {
  plan: BillingPlan;
  subscription: BillingSubscription;
  usage: BillingUsage;
  payment_mode: string;
}

export interface CheckoutResponse {
  provider: string;
  mode: string;
  plan_slug: string;
  checkout_type: "local_test" | "razorpay_subscription" | string;
  test_checkout_url: string | null;
  key_id: string | null;
  subscription_id: string | null;
  order_id: string | null;
  amount: number | null;
  currency: string;
  name: string | null;
  description: string | null;
  prefill: {
    email?: string | null;
    name?: string | null;
  } | null;
  message: string;
}

export async function getPlans(): Promise<BillingPlan[]> {
  const response = await apiClient.get<BillingPlan[]>("/billing/plans");
  return response.data;
}

export async function getMyBilling(): Promise<MyBilling> {
  const response = await apiClient.get<MyBilling>("/billing/me");
  return response.data;
}

export async function createCheckout(
  planSlug: string,
): Promise<CheckoutResponse> {
  const response = await apiClient.post<CheckoutResponse>("/billing/checkout", {
    plan_slug: planSlug,
  });
  return response.data;
}

export async function activateTestPlan(
  planSlug: string,
): Promise<BillingSubscription> {
  const response = await apiClient.post<BillingSubscription>(
    "/billing/test/activate",
    { plan_slug: planSlug },
  );
  return response.data;
}

export async function cancelSubscription(): Promise<BillingSubscription> {
  const response = await apiClient.post<BillingSubscription>("/billing/cancel", {});
  return response.data;
}

export async function getUsage(): Promise<BillingUsage> {
  const response = await apiClient.get<BillingUsage>("/billing/usage");
  return response.data;
}
