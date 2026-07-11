export type WorkflowRunStatus =
  | "pending"
  | "running"
  | "succeeded"
  | "failed"
  | "cancelled";

export type WorkflowRunTrigger = "manual" | "api" | "simulated" | "scheduled";
export type ModelCallStatus =
  | "pending"
  | "succeeded"
  | "failed"
  | "retried"
  | "fallback_used";
export type ToolCallStatus = "pending" | "succeeded" | "failed";

export interface WorkflowRun {
  id: string;
  project_id: string;
  workflow_id: string;
  configuration_id: string | null;
  triggered_by_user_id: string | null;
  trigger_type: WorkflowRunTrigger;
  external_reference: string | null;
  status: WorkflowRunStatus;
  input_summary: string | null;
  output_summary: string | null;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  latency_ms: number | null;
  metadata_json: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface StartWorkflowRunInput {
  project_id: string;
  workflow_id: string;
  configuration_id?: string | null;
  trigger_type?: WorkflowRunTrigger;
  external_reference?: string;
  input_summary?: string;
  metadata_json?: Record<string, unknown>;
}

export interface ModelCallInput {
  sequence_number: number;
  provider: string;
  model_name: string;
  call_type?: string;
  status?: ModelCallStatus;
  prompt_tokens?: number;
  completion_tokens?: number;
  total_tokens?: number;
  latency_ms?: number;
  estimated_cost_usd?: number;
  is_retry?: boolean;
  is_fallback?: boolean;
  request_summary?: string;
  response_summary?: string;
  error_message?: string;
  metadata_json?: Record<string, unknown>;
}

export interface ToolCallInput {
  sequence_number: number;
  tool_name: string;
  status?: ToolCallStatus;
  latency_ms?: number;
  estimated_cost_usd?: number;
  input_summary?: string;
  output_summary?: string;
  error_message?: string;
  metadata_json?: Record<string, unknown>;
}

export interface WorkflowRunTrace {
  workflow_run: WorkflowRun;
  model_calls: Array<ModelCallInput & { id: string; workflow_run_id: string }>;
  tool_calls: Array<ToolCallInput & { id: string; workflow_run_id: string }>;
}
