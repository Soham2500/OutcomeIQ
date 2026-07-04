export type DecimalValue = number | string;

export interface DashboardOverview {
  project_id: string;
  total_workflows: number;
  total_workflow_runs: number;
  succeeded_runs: number;
  failed_runs: number;
  pending_runs: number;
  total_cost_usd: DecimalValue;
  successful_outcomes: number;
  failed_outcomes: number;
  success_rate: DecimalValue;
  cost_per_successful_outcome_usd: DecimalValue | null;
  notes: string | null;
}

export interface DashboardWorkflowRun {
  workflow_run_id: string;
  workflow_id: string;
  workflow_name: string | null;
  configuration_id: string | null;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  total_cost_usd: DecimalValue | null;
  outcome_status: string | null;
  success: boolean | null;
}

export interface CostSummary {
  project_id: string;
  total_cost_usd: DecimalValue;
  model_cost_usd: DecimalValue;
  tool_cost_usd: DecimalValue;
  total_tokens: number;
  model_call_count: number;
  tool_call_count: number;
  average_cost_per_run_usd: DecimalValue;
  highest_cost_run_id: string | null;
}

export interface OutcomeSummary {
  project_id: string;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  pending_runs: number;
  success_rate: DecimalValue;
  cost_per_successful_outcome_usd: DecimalValue | null;
}

export interface DashboardData {
  overview: DashboardOverview;
  workflowRuns: DashboardWorkflowRun[];
  costSummary: CostSummary;
  outcomeSummary: OutcomeSummary;
}
