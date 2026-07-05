import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../api/client";
import { getProjectDashboard } from "../api/dashboardApi";
import { listProjects } from "../api/projectsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { StatCard } from "../components/StatCard";
import { CostByRunChart } from "../components/charts/CostByRunChart";
import { CostOutcomeInsight } from "../components/charts/CostOutcomeInsight";
import { OutcomeStatusChart } from "../components/charts/OutcomeStatusChart";
import { SuccessRateCard } from "../components/charts/SuccessRateCard";
import type { DashboardData } from "../types/dashboard";
import type { Project } from "../types/project";
import { formatDateTime, formatUsd } from "../utils/formatters";

export function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function loadProjectOptions() {
    setLoadingProjects(true);
    setError(null);
    try {
      const items = await listProjects();
      setProjects(items);
      setSelectedProjectId((current) => current || items[0]?.id || "");
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Projects could not be loaded."));
    } finally {
      setLoadingProjects(false);
    }
  }

  async function loadDashboard(projectId: string) {
    if (!projectId) {
      setDashboard(null);
      return;
    }
    setLoadingDashboard(true);
    setError(null);
    try {
      setDashboard(await getProjectDashboard(projectId));
    } catch (requestError) {
      setDashboard(null);
      setError(
        getApiErrorMessage(requestError, "Dashboard data could not be loaded."),
      );
    } finally {
      setLoadingDashboard(false);
    }
  }

  useEffect(() => {
    void loadProjectOptions();
  }, []);

  useEffect(() => {
    void loadDashboard(selectedProjectId);
  }, [selectedProjectId]);

  if (loadingProjects) {
    return <LoadingState message="Loading projects…" />;
  }

  if (error && projects.length === 0) {
    return <ErrorState message={error} onRetry={() => void loadProjectOptions()} />;
  }

  if (projects.length === 0) {
    return (
      <EmptyState
        action={
          <Link className="primary-button" to="/projects">
            Create a project
          </Link>
        }
        description="Create an organization and project before viewing outcome-aware workflow economics."
        title="No projects yet"
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-500">
            Cost, outcome and unit-economics evidence for AI workflows.
          </p>
        </div>
        <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row sm:items-end">
          <label className="w-full sm:w-72">
            <span className="field-label">Project</span>
            <select
              className="field-input"
              onChange={(event) => setSelectedProjectId(event.target.value)}
              value={selectedProjectId}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
          <button
            className="secondary-button"
            disabled={loadingDashboard || !selectedProjectId}
            onClick={() => void loadDashboard(selectedProjectId)}
            type="button"
          >
            {loadingDashboard ? "Refreshing…" : "Refresh"}
          </button>
        </div>
      </div>

      {error ? (
        <ErrorState
          message={error}
          onRetry={() => void loadDashboard(selectedProjectId)}
        />
      ) : null}
      {loadingDashboard ? (
        <LoadingState message="Calculating project analytics…" />
      ) : null}

      {!loadingDashboard && dashboard ? (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard
              label="Total workflow runs"
              value={dashboard.overview.total_workflow_runs ?? 0}
            />
            <StatCard
              label="Total cost"
              value={formatUsd(
                dashboard.costSummary.total_cost_usd ??
                  dashboard.overview.total_cost_usd,
              )}
            />
            <SuccessRateCard successRate={dashboard.outcomeSummary.success_rate} />
            <StatCard
              hint="Outcome-aware unit economics"
              label="Cost per successful outcome"
              value={formatUsd(
                dashboard.outcomeSummary.cost_per_successful_outcome_usd,
              )}
            />
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <CostByRunChart runs={dashboard.workflowRuns} />
            <OutcomeStatusChart
              failed={dashboard.outcomeSummary.failed_runs}
              pending={dashboard.outcomeSummary.pending_runs}
              successful={dashboard.outcomeSummary.successful_runs}
            />
          </section>

          <CostOutcomeInsight
            costPerSuccessfulOutcome={
              dashboard.outcomeSummary.cost_per_successful_outcome_usd
            }
            successfulOutcomes={dashboard.overview.successful_outcomes ?? 0}
            totalCost={
              dashboard.costSummary.total_cost_usd ?? dashboard.overview.total_cost_usd
            }
          />

          <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card">
            <div className="border-b border-slate-200 px-5 py-4">
              <h2 className="font-semibold text-slate-900">Recent workflow runs</h2>
              <p className="mt-1 text-sm text-slate-500">
                Technical status, recorded cost and verified business outcome.
              </p>
            </div>
            {dashboard.workflowRuns.length === 0 ? (
              <div className="p-6">
                <EmptyState
                  description="Seed demo data or record workflow telemetry to populate this table."
                  title="No workflow runs recorded"
                />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-5 py-3 font-medium">Run</th>
                      <th className="px-5 py-3 font-medium">Status</th>
                      <th className="px-5 py-3 font-medium">Cost</th>
                      <th className="px-5 py-3 font-medium">Outcome</th>
                      <th className="px-5 py-3 font-medium">Started</th>
                      <th className="px-5 py-3 font-medium">Completed</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {dashboard.workflowRuns.map((run, index) => (
                      <tr key={run.workflow_run_id ?? `run-${index}`}>
                        <td className="whitespace-nowrap px-5 py-3 font-mono text-xs text-slate-700">
                          {run.workflow_run_id?.slice(0, 8) ?? `Run ${index + 1}`}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 capitalize text-slate-700">
                          {(run.status || "unknown").replaceAll("_", " ")}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-slate-700">
                          {formatUsd(run.total_cost_usd)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 capitalize text-slate-700">
                          {run.outcome_status?.replaceAll("_", " ") ??
                            "Pending evidence"}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDateTime(run.started_at)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDateTime(run.completed_at)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      ) : null}
    </div>
  );
}
