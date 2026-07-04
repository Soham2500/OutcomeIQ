import { apiClient } from "./client";
import type {
  Recommendation,
  RecommendationGenerateResponse,
  RecommendationStatus,
} from "../types/recommendation";

export async function listRecommendations(
  projectId: string,
): Promise<Recommendation[]> {
  const response = await apiClient.get<Recommendation[]>("/recommendations", {
    params: { project_id: projectId },
  });
  return response.data;
}

export async function generateRecommendations(
  projectId: string,
): Promise<RecommendationGenerateResponse> {
  const response = await apiClient.post<RecommendationGenerateResponse>(
    "/recommendations/generate",
    { project_id: projectId },
  );
  return response.data;
}

export async function updateRecommendationStatus(
  recommendationId: string,
  status: RecommendationStatus,
): Promise<Recommendation> {
  const response = await apiClient.patch<Recommendation>(
    `/recommendations/${recommendationId}`,
    { status },
  );
  return response.data;
}
