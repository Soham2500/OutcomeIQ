import { apiClient } from "./client";
import type {
  CreatePricingRateInput,
  ModelPricingRate,
  WorkflowRunCost,
} from "../types/cost";

export async function calculateWorkflowRunCost(
  workflowRunId: string,
): Promise<WorkflowRunCost> {
  const response = await apiClient.post<WorkflowRunCost>(
    `/costs/workflow-runs/${workflowRunId}/calculate`,
    {},
  );
  return response.data;
}

export async function getWorkflowRunCost(
  workflowRunId: string,
): Promise<WorkflowRunCost> {
  const response = await apiClient.get<WorkflowRunCost>(
    `/costs/workflow-runs/${workflowRunId}`,
  );
  return response.data;
}

export async function listPricingRates(
  provider?: string,
): Promise<ModelPricingRate[]> {
  const response = await apiClient.get<ModelPricingRate[]>("/costs/pricing-rates", {
    params: provider ? { provider } : undefined,
  });
  return response.data;
}

export async function createPricingRate(
  request: CreatePricingRateInput,
): Promise<ModelPricingRate> {
  const response = await apiClient.post<ModelPricingRate>(
    "/costs/pricing-rates",
    request,
  );
  return response.data;
}
