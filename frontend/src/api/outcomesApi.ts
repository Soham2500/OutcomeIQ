import { apiClient } from "./client";
import type {
  CostPerSuccessfulOutcomeMetric,
  CreateOutcomeContractInput,
  OutcomeContract,
  RecordWorkflowRunOutcomeInput,
  WorkflowRunOutcome,
} from "../types/outcome";

export async function createOutcomeContract(
  request: CreateOutcomeContractInput,
): Promise<OutcomeContract> {
  const response = await apiClient.post<OutcomeContract>(
    "/outcomes/contracts",
    request,
  );
  return response.data;
}

export async function listOutcomeContracts(params?: {
  project_id?: string;
  workflow_id?: string;
}): Promise<OutcomeContract[]> {
  const response = await apiClient.get<OutcomeContract[]>("/outcomes/contracts", {
    params,
  });
  return response.data;
}

export async function recordWorkflowRunOutcome(
  workflowRunId: string,
  request: RecordWorkflowRunOutcomeInput,
): Promise<WorkflowRunOutcome> {
  const response = await apiClient.post<WorkflowRunOutcome>(
    `/outcomes/workflow-runs/${workflowRunId}`,
    request,
  );
  return response.data;
}

export async function getWorkflowRunOutcome(
  workflowRunId: string,
): Promise<WorkflowRunOutcome> {
  const response = await apiClient.get<WorkflowRunOutcome>(
    `/outcomes/workflow-runs/${workflowRunId}`,
  );
  return response.data;
}

export async function getCostPerSuccessfulOutcome(params?: {
  project_id?: string;
  workflow_id?: string;
  configuration_id?: string;
}): Promise<CostPerSuccessfulOutcomeMetric> {
  const response = await apiClient.get<CostPerSuccessfulOutcomeMetric>(
    "/outcomes/metrics/cost-per-success",
    { params },
  );
  return response.data;
}
