import { apiClient } from "./client";
import type {
  CreateOrganizationInput,
  CreateProjectInput,
  Organization,
  Project,
} from "../types/project";

type ProjectListResponse =
  | Project[]
  | { items?: Project[]; projects?: Project[]; data?: Project[] | { items?: Project[] } };

function normalizeProjectList(payload: ProjectListResponse): Project[] {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (Array.isArray(payload.items)) {
    return payload.items;
  }
  if (Array.isArray(payload.projects)) {
    return payload.projects;
  }
  if (Array.isArray(payload.data)) {
    return payload.data;
  }
  if (payload.data && !Array.isArray(payload.data) && Array.isArray(payload.data.items)) {
    return payload.data.items;
  }
  return [];
}

export async function listProjects(): Promise<Project[]> {
  const response = await apiClient.get<ProjectListResponse>("/projects");
  return normalizeProjectList(response.data);
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
