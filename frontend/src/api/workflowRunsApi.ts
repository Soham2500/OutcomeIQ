import { apiClient } from "./client";
import type {
  ModelCallInput,
  StartWorkflowRunInput,
  ToolCallInput,
  WorkflowRun,
  WorkflowRunTrace,
} from "../types/workflowRun";

export async function startWorkflowRun(
  request: StartWorkflowRunInput,
): Promise<WorkflowRun> {
  const response = await apiClient.post<WorkflowRun>("/workflow-runs", request);
  return response.data;
}

export async function recordModelCall(
  workflowRunId: string,
  request: ModelCallInput,
): Promise<ModelCallInput & { id: string; workflow_run_id: string }> {
  const response = await apiClient.post<
    ModelCallInput & { id: string; workflow_run_id: string }
  >(`/workflow-runs/${workflowRunId}/model-calls`, request);
  return response.data;
}

export async function recordToolCall(
  workflowRunId: string,
  request: ToolCallInput,
): Promise<ToolCallInput & { id: string; workflow_run_id: string }> {
  const response = await apiClient.post<
    ToolCallInput & { id: string; workflow_run_id: string }
  >(`/workflow-runs/${workflowRunId}/tool-calls`, request);
  return response.data;
}

export async function completeWorkflowRun(
  workflowRunId: string,
  request: { output_summary?: string; latency_ms?: number } = {},
): Promise<WorkflowRun> {
  const response = await apiClient.post<WorkflowRun>(
    `/workflow-runs/${workflowRunId}/complete`,
    request,
  );
  return response.data;
}

export async function failWorkflowRun(
  workflowRunId: string,
  request: { error_message?: string; latency_ms?: number } = {},
): Promise<WorkflowRun> {
  const response = await apiClient.post<WorkflowRun>(
    `/workflow-runs/${workflowRunId}/fail`,
    request,
  );
  return response.data;
}

export async function getWorkflowTrace(
  workflowRunId: string,
): Promise<WorkflowRunTrace> {
  const response = await apiClient.get<WorkflowRunTrace>(
    `/workflow-runs/${workflowRunId}/trace`,
  );
  return response.data;
}
