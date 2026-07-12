import { apiClient } from "./client";
import type { AiRun, AiRunCreatePayload } from "../types/aiRun";

export async function createAiRun(payload: AiRunCreatePayload): Promise<AiRun> {
  const response = await apiClient.post<AiRun>("/ai/runs", payload);
  return response.data;
}

export async function listAiRuns(projectId?: string): Promise<AiRun[]> {
  const response = await apiClient.get<AiRun[]>("/ai/runs", {
    params: projectId ? { project_id: projectId } : undefined,
  });
  return response.data;
}
