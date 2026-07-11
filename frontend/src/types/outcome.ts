import type { DecimalValue } from "./dashboard";

export type OutcomeStatus =
  | "pending"
  | "succeeded"
  | "failed"
  | "escalated"
  | "reopened"
  | "abandoned"
  | "reversed";

export interface OutcomeContract {
  id: string;
  project_id: string;
  workflow_id: string | null;
  name: string;
  description: string | null;
  success_criteria_json: Record<string, unknown> | null;
  success_window_hours: number;
  status: "active" | "inactive" | "archived";
  created_by_user_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateOutcomeContractInput {
  project_id: string;
  workflow_id?: string | null;
  name: string;
  description?: string;
  success_criteria_json?: Record<string, unknown>;
  success_window_hours?: number;
}

export interface WorkflowRunOutcome {
  id: string;
  workflow_run_id: string;
  outcome_contract_id: string | null;
  status: OutcomeStatus;
  verification_source: "manual" | "simulated" | "api" | "system";
  outcome_score: DecimalValue | null;
  business_value_usd: DecimalValue | null;
  verified_at: string | null;
  notes: string | null;
  metadata_json: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface RecordWorkflowRunOutcomeInput {
  outcome_contract_id?: string | null;
  status: OutcomeStatus;
  verification_source?: "manual" | "simulated" | "api" | "system";
  outcome_score?: number;
  business_value_usd?: number;
  verified_at?: string;
  notes?: string;
  metadata_json?: Record<string, unknown>;
}

export interface CostPerSuccessfulOutcomeMetric {
  project_id: string | null;
  workflow_id: string | null;
  configuration_id: string | null;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  pending_runs: number;
  total_cost_usd: DecimalValue;
  cost_per_successful_outcome_usd: DecimalValue | null;
  success_rate: DecimalValue;
  notes: string | null;
}
