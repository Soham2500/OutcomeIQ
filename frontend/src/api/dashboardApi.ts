import { apiClient } from "./client";
import type {
  CostSummary,
  DashboardData,
  DashboardOverview,
  DashboardWorkflowRun,
  OutcomeSummary,
} from "../types/dashboard";

function dashboardPath(projectId: string, resource: string): string {
  return `/dashboard/projects/${encodeURIComponent(projectId)}/${resource}`;
}

export async function getProjectOverview(
  projectId: string,
): Promise<DashboardOverview> {
  const response = await apiClient.get<DashboardOverview>(
    dashboardPath(projectId, "overview"),
  );
  return response.data;
}

export async function getProjectWorkflowRuns(
  projectId: string,
  limit = 50,
  offset = 0,
): Promise<DashboardWorkflowRun[]> {
  const response = await apiClient.get<DashboardWorkflowRun[]>(
    dashboardPath(projectId, "workflow-runs"),
    { params: { limit, offset } },
  );
  return response.data;
}

export async function getProjectCostSummary(
  projectId: string,
): Promise<CostSummary> {
  const response = await apiClient.get<CostSummary>(
    dashboardPath(projectId, "cost-summary"),
  );
  return response.data;
}

export async function getProjectOutcomeSummary(
  projectId: string,
): Promise<OutcomeSummary> {
  const response = await apiClient.get<OutcomeSummary>(
    dashboardPath(projectId, "outcome-summary"),
  );
  return response.data;
}

export async function getProjectDashboard(
  projectId: string,
): Promise<DashboardData> {
  const [overview, workflowRuns, costSummary, outcomeSummary] =
    await Promise.all([
      getProjectOverview(projectId),
      getProjectWorkflowRuns(projectId),
      getProjectCostSummary(projectId),
      getProjectOutcomeSummary(projectId),
    ]);

  return {
    overview,
    workflowRuns,
    costSummary,
    outcomeSummary,
  };
}
