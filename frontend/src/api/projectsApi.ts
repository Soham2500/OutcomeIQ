import { apiClient } from "./client";
import type {
  CreateOrganizationInput,
  CreateProjectInput,
  Organization,
  Project,
} from "../types/project";

export async function listProjects(): Promise<Project[]> {
  const response = await apiClient.get<Project[]>("/projects");
  return response.data;
}

export async function createOrganization(
  request: CreateOrganizationInput,
): Promise<Organization> {
  const response = await apiClient.post<Organization>("/organizations", request);
  return response.data;
}

export async function createProject(
  request: CreateProjectInput,
): Promise<Project> {
  const response = await apiClient.post<Project>("/projects", request);
  return response.data;
}
