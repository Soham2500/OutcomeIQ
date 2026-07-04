import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getProjectDashboard } from "../api/dashboardApi";
import { getApiErrorMessage } from "../api/client";
import { listProjects } from "../api/projectsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { StatCard } from "../components/StatCard";
import type { DashboardData, DecimalValue } from "../types/dashboard";
import type { Project } from "../types/project";

function asNumber(value: DecimalValue | null): number | null {
  if (value === null) {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatUsd(value: DecimalValue | null): string {
  const parsed = asNumber(value);
  if (parsed === null) {
    return "—";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: parsed < 0.01 ? 4 : 2,
    maximumFractionDigits: parsed < 0.01 ? 6 : 2,
  }).format(parsed);
}

function formatRate(value: DecimalValue): string {
  const parsed = asNumber(value) ?? 0;
  return `${(parsed * 100).toFixed(1)}%`;
}

function formatDate(value: string | null): string {
  return value ? new Date(value).toLocaleString() : "—";
}

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

  useEffect(() => {
    void loadProjectOptions();
  }, []);

  useEffect(() => {
    if (!selectedProjectId) {
      setDashboard(null);
      return;
    }

    let active = true;
    setLoadingDashboard(true);
    setError(null);
    getProjectDashboard(selectedProjectId)
      .then((data) => {
        if (active) {
          setDashboard(data);
        }
      })
      .catch((requestError: unknown) => {
        if (active) {
          setDashboard(null);
          setError(
            getApiErrorMessage(requestError, "Dashboard data could not be loaded."),
          );
        }
      })
      .finally(() => {
        if (active) {
          setLoadingDashboard(false);
        }
      });

    return () => {
      active = false;
    };
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
      </div>

      {error ? <ErrorState message={error} /> : null}
      {loadingDashboard ? <LoadingState message="Calculating project analytics…" /> : null}

      {!loadingDashboard && dashboard ? (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            <StatCard label="Total workflow runs" value={dashboard.overview.total_workflow_runs} />
            <StatCard label="Total cost" value={formatUsd(dashboard.costSummary.total_cost_usd)} />
            <StatCard label="Success rate" value={formatRate(dashboard.outcomeSummary.success_rate)} />
            <StatCard
              hint="Outcome-aware unit economics"
              label="Cost per successful outcome"
              value={formatUsd(dashboard.outcomeSummary.cost_per_successful_outcome_usd)}
            />
            <StatCard label="Successful outcomes" value={dashboard.overview.successful_outcomes} />
            <StatCard label="Failed outcomes" value={dashboard.overview.failed_outcomes} />
          </section>

          <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-card">
            <div className="border-b border-slate-200 px-5 py-4">
              <h2 className="font-semibold text-slate-900">Recent workflow runs</h2>
              <p className="mt-1 text-sm text-slate-500">
                Technical status, recorded cost and verified business outcome.
              </p>
            </div>
            {dashboard.workflowRuns.length === 0 ? (
              <div className="p-8 text-center text-sm text-slate-500">
                No workflow runs have been recorded for this project.
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
                    {dashboard.workflowRuns.map((run) => (
                      <tr key={run.workflow_run_id}>
                        <td className="whitespace-nowrap px-5 py-3 font-mono text-xs text-slate-700">
                          {run.workflow_run_id.slice(0, 8)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 capitalize text-slate-700">
                          {run.status.replaceAll("_", " ")}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-slate-700">
                          {formatUsd(run.total_cost_usd)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 capitalize text-slate-700">
                          {run.outcome_status?.replaceAll("_", " ") ?? "Pending evidence"}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDate(run.started_at)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDate(run.completed_at)}
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
