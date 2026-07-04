import { apiClient } from "./client";
import type {
  CostSummary,
  DashboardData,
  DashboardOverview,
  DashboardWorkflowRun,
  OutcomeSummary,
} from "../types/dashboard";

export async function getProjectDashboard(
  projectId: string,
): Promise<DashboardData> {
  const basePath = `/dashboard/projects/${projectId}`;
  const [overview, workflowRuns, costSummary, outcomeSummary] =
    await Promise.all([
      apiClient.get<DashboardOverview>(`${basePath}/overview`),
      apiClient.get<DashboardWorkflowRun[]>(`${basePath}/workflow-runs`),
      apiClient.get<CostSummary>(`${basePath}/cost-summary`),
      apiClient.get<OutcomeSummary>(`${basePath}/outcome-summary`),
    ]);

  return {
    overview: overview.data,
    workflowRuns: workflowRuns.data,
    costSummary: costSummary.data,
    outcomeSummary: outcomeSummary.data,
  };
}
