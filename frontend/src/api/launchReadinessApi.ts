import { apiClient } from "./client";

export interface LaunchReadiness {
  app_env: string;
  debug_disabled: boolean;
  cors_configured: boolean;
  database_configured: boolean;
  payments_live_enabled: boolean;
  razorpay_test_configured: boolean;
  policy_pages_expected: boolean;
  support_email_configured: boolean;
  admin_emails_configured: boolean;
  openai_live_enabled: boolean;
  note: string;
}

export async function getLaunchReadiness(): Promise<LaunchReadiness> {
  const response = await apiClient.get<LaunchReadiness>("/launch/readiness");
  return response.data;
}
