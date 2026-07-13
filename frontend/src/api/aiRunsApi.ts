import { apiClient, isApiStatus } from "./client";
import type { AiRun, AiRunCreatePayload } from "../types/aiRun";

type AiRunListResponse =
  | AiRun[]
  | { items?: AiRun[]; runs?: AiRun[]; data?: AiRun[] | { items?: AiRun[] } };

function normalizeAiRunList(payload: AiRunListResponse): AiRun[] {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (Array.isArray(payload.items)) {
    return payload.items;
  }
  if (Array.isArray(payload.runs)) {
    return payload.runs;
  }
  if (Array.isArray(payload.data)) {
    return payload.data;
  }
  if (payload.data && !Array.isArray(payload.data) && Array.isArray(payload.data.items)) {
    return payload.data.items;
  }
  return [];
}

export async function createAiRun(payload: AiRunCreatePayload): Promise<AiRun> {
  const response = await apiClient.post<AiRun>("/ai/runs", payload);
  return response.data;
}

export async function listAiRuns(projectId?: string): Promise<AiRun[]> {
  try {
    const response = await apiClient.get<AiRunListResponse>("/ai/runs", {
      params: projectId ? { project_id: projectId } : undefined,
    });
    return normalizeAiRunList(response.data);
  } catch (error) {
    if (isApiStatus(error, 404)) {
      console.info("[OutcomeIQ AI runs] Optional run list endpoint returned 404; showing empty state.");
      return [];
    }
    throw error;
  }
}
