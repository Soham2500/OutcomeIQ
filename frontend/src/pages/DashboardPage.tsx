import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../api/client";
import { getProjectDashboard } from "../api/dashboardApi";
import { runDemoScenario } from "../api/demoApi";
import { listProjects } from "../api/projectsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { StatCard } from "../components/StatCard";
import type { DashboardData } from "../types/dashboard";
import type { Project } from "../types/project";
import { formatDateTime, formatPercent, formatUsd, shortId } from "../utils/format";

export function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

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
        getApiErrorMessage(
          requestError,
          "Could not load dashboard data. Check backend and demo setup.",
        ),
      );
    } finally {
      setLoadingDashboard(false);
    }
  }

  async function handleRunDemo() {
    setRunningDemo(true);
    setError(null);
    setSuccess(null);
    try {
      await runDemoScenario(selectedProjectId);
      setSuccess("Demo data created. Dashboard refreshed with workflow costs and outcomes.");
      await loadDashboard(selectedProjectId);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Demo data could not be created."));
    } finally {
      setRunningDemo(false);
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

  const totalRuns = dashboard?.overview.total_workflow_runs ?? 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-500">
            Cost, outcome and unit-economics evidence for AI workflows.
          </p>
        </div>
        <div className="flex w-full flex-col gap-3 lg:w-auto lg:flex-row lg:items-end">
          <label className="w-full lg:w-72">
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
            {loadingDashboard ? "Refreshing…" : "Refresh Dashboard"}
          </button>
          <button
            className="primary-button"
            disabled={runningDemo || !selectedProjectId}
            onClick={() => void handleRunDemo()}
            type="button"
          >
            {runningDemo ? "Creating demo data…" : "Run Demo Data"}
          </button>
        </div>
      </div>

      {success ? (
        <p className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
          {success}
        </p>
      ) : null}
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
            <StatCard label="Total workflow runs" value={totalRuns} />
            <StatCard
              label="Total cost USD"
              value={formatUsd(
                dashboard.costSummary.total_cost_usd ??
                  dashboard.overview.total_cost_usd,
              )}
            />
            <StatCard
              label="Success rate"
              value={formatPercent(dashboard.outcomeSummary.success_rate)}
            />
            <StatCard
              hint="Outcome-aware unit economics"
              label="Cost per successful outcome"
              value={formatUsd(
                dashboard.outcomeSummary.cost_per_successful_outcome_usd,
              )}
            />
            <StatCard
              label="Successful outcomes"
              value={dashboard.outcomeSummary.successful_runs}
            />
            <StatCard
              label="Failed outcomes"
              value={dashboard.outcomeSummary.failed_runs}
            />
            <StatCard
              label="Pending outcomes"
              value={dashboard.outcomeSummary.pending_runs}
            />
            <StatCard
              hint="Model + tool telemetry"
              label="Tracked calls"
              value={
                dashboard.costSummary.model_call_count +
                dashboard.costSummary.tool_call_count
              }
            />
          </section>

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
                  action={
                    <button
                      className="primary-button"
                      disabled={runningDemo}
                      onClick={() => void handleRunDemo()}
                      type="button"
                    >
                      {runningDemo ? "Creating demo data…" : "Run Demo Data"}
                    </button>
                  }
                  description="No workflow runs yet. Generate simulated support-ticket data to see cost per successful outcome."
                  title="No workflow runs yet"
                />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-5 py-3 font-medium">Run ID</th>
                      <th className="px-5 py-3 font-medium">Status</th>
                      <th className="px-5 py-3 font-medium">Cost</th>
                      <th className="px-5 py-3 font-medium">Outcome</th>
                      <th className="px-5 py-3 font-medium">Started at</th>
                      <th className="px-5 py-3 font-medium">Completed at</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {dashboard.workflowRuns.map((run, index) => (
                      <tr key={run.workflow_run_id ?? `run-${index}`}>
                        <td className="whitespace-nowrap px-5 py-3 font-mono text-xs text-slate-700">
                          {run.workflow_run_id
                            ? shortId(run.workflow_run_id)
                            : `Run ${index + 1}`}
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
