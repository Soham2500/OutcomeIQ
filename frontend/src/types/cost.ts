import type { DecimalValue } from "./dashboard";

export interface WorkflowRunCost {
  id: string;
  workflow_run_id: string;
  currency: string;
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
  model_call_count: number;
  tool_call_count: number;
  model_cost_usd: DecimalValue;
  tool_cost_usd: DecimalValue;
  total_cost_usd: DecimalValue;
  calculation_status: "calculated" | "partial" | "failed";
  calculation_notes: string | null;
  calculated_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ModelPricingRate {
  id: string;
  provider: string;
  model_name: string;
  currency: string;
  input_token_price_per_1k: DecimalValue;
  output_token_price_per_1k: DecimalValue;
  effective_from: string | null;
  effective_to: string | null;
  is_active: boolean;
  metadata_json: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePricingRateInput {
  provider: string;
  model_name: string;
  currency?: string;
  input_token_price_per_1k: number;
  output_token_price_per_1k: number;
  is_active?: boolean;
  metadata_json?: Record<string, unknown>;
}
