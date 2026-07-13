export type DecimalValue = number | string;

export interface DashboardOverview {
  project_id: string;
  total_workflows: number;
  total_workflow_runs?: number;
  succeeded_runs: number;
  failed_runs: number;
  pending_runs: number;
  total_cost_usd?: DecimalValue | null;
  total_cost_inr?: DecimalValue | null;
  successful_outcomes: number;
  failed_outcomes: number;
  success_rate?: DecimalValue | null;
  cost_per_successful_outcome_usd?: DecimalValue | null;
  cost_per_successful_outcome_inr?: DecimalValue | null;
  notes: string | null;
}

export interface DashboardWorkflowRun {
  workflow_run_id?: string;
  workflow_id: string;
  workflow_name: string | null;
  configuration_id: string | null;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  total_cost_usd?: DecimalValue | null;
  total_cost_inr?: DecimalValue | null;
  outcome_status?: string | null;
  success: boolean | null;
}

export interface CostSummary {
  project_id: string;
  total_cost_usd?: DecimalValue | null;
  total_cost_inr?: DecimalValue | null;
  model_cost_usd: DecimalValue;
  tool_cost_usd: DecimalValue;
  ai_cost_usd: DecimalValue;
  ai_cost_inr: DecimalValue;
  total_tokens: number;
  ai_total_tokens: number;
  model_call_count: number;
  tool_call_count: number;
  ai_run_count: number;
  average_cost_per_run_usd: DecimalValue;
  average_cost_per_run_inr?: DecimalValue | null;
  highest_cost_run_id: string | null;
  cost_by_provider: AiCostBreakdown[];
  cost_by_model: AiCostBreakdown[];
  latest_ai_runs: LatestAiRunDashboard[];
}

export interface AiCostBreakdown {
  key: string;
  total_cost_inr: DecimalValue;
  total_cost_usd: DecimalValue;
  total_tokens: number;
  run_count: number;
}

export interface LatestAiRunDashboard {
  id: string;
  provider: string;
  model: string;
  workflow_name: string;
  total_tokens: number;
  cost_inr: DecimalValue;
  latency_ms: number;
  status: string;
  created_at: string;
}

export interface OutcomeSummary {
  project_id: string;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  pending_runs: number;
  success_rate?: DecimalValue | null;
  cost_per_successful_outcome_usd?: DecimalValue | null;
  cost_per_successful_outcome_inr?: DecimalValue | null;
}

export interface DashboardData {
  overview: DashboardOverview;
  workflowRuns: DashboardWorkflowRun[];
  costSummary: CostSummary;
  outcomeSummary: OutcomeSummary;
}
