import type { DecimalValue } from "./dashboard";

export type RecommendationSeverity = "low" | "medium" | "high";
export type RecommendationStatus =
  | "open"
  | "accepted"
  | "dismissed"
  | "resolved";

export interface Recommendation {
  id: string;
  project_id: string;
  workflow_id: string | null;
  recommendation_type: string;
  severity: RecommendationSeverity;
  status: RecommendationStatus;
  title: string;
  description: string | null;
  current_metric_json: Record<string, unknown> | null;
  suggested_action_json: Record<string, unknown> | null;
  potential_savings_usd: DecimalValue | null;
  confidence_score: DecimalValue | null;
  generated_at: string | null;
  accepted_at: string | null;
  dismissed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface RecommendationGenerateResponse {
  project_id: string;
  workflow_id: string | null;
  generated_count: number;
  recommendations: Recommendation[];
}
