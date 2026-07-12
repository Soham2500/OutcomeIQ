export type AiProvider = "gemini" | "openai";

export interface AiRunCreatePayload {
  project_id: string;
  workflow_name: string;
  prompt: string;
  provider?: AiProvider;
  model?: string;
}

export interface AiRun {
  id: string;
  project_id: string;
  workflow_name: string;
  provider: AiProvider;
  model: string;
  response_text?: string | null;
  prompt_preview: string;
  response_preview?: string | null;
  status: string;
  error_message?: string | null;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  cost_usd: string;
  cost_inr: string;
  currency: string;
  pricing_unknown: boolean;
  latency_ms: number;
  created_at: string;
}
