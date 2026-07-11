import { apiClient } from "./client";
import type {
  CreateWorkflowConfigurationInput,
  CreateWorkflowInput,
  Workflow,
  WorkflowConfiguration,
} from "../types/workflow";

export async function createWorkflow(
  request: CreateWorkflowInput,
): Promise<Workflow> {
  const response = await apiClient.post<Workflow>("/workflows", request);
  return response.data;
}

export async function listWorkflows(projectId?: string): Promise<Workflow[]> {
  const response = await apiClient.get<Workflow[]>("/workflows", {
    params: projectId ? { project_id: projectId } : undefined,
  });
  return response.data;
}

export async function createWorkflowConfiguration(
  workflowId: string,
  request: CreateWorkflowConfigurationInput,
): Promise<WorkflowConfiguration> {
  const response = await apiClient.post<WorkflowConfiguration>(
    `/workflows/${workflowId}/configurations`,
    request,
  );
  return response.data;
}

export async function listWorkflowConfigurations(
  workflowId: string,
): Promise<WorkflowConfiguration[]> {
  const response = await apiClient.get<WorkflowConfiguration[]>(
    `/workflows/${workflowId}/configurations`,
  );
  return response.data;
}
