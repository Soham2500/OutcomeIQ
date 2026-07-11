import { useEffect, useMemo, useState } from "react";
import { getApiErrorMessage } from "../api/client";
import { getProjectDashboard } from "../api/dashboardApi";
import { runDemoScenario } from "../api/demoApi";
import { listProjects } from "../api/projectsApi";
import { listRecommendations } from "../api/recommendationsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { MetricBar } from "../components/MetricBar";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";
import { StatCard } from "../components/StatCard";
import type { DashboardData } from "../types/dashboard";
import type { Project } from "../types/project";
import type { Recommendation } from "../types/recommendation";
import {
  exportProjectSummaryAsCsv,
  exportProjectSummaryAsJson,
} from "../utils/exportUtils";
import { formatPercent, formatUsd, toFiniteNumber } from "../utils/format";

export function AnalyticsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingAnalytics, setLoadingAnalytics] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);

  const selectedProject = projects.find((project) => project.id === selectedProjectId);

  async function loadProjects() {
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

  async function loadAnalytics(projectId: string) {
    if (!projectId) {
      setDashboard(null);
      setRecommendations([]);
      return;
    }
    setLoadingAnalytics(true);
    setError(null);
    try {
      const [dashboardData, recommendationData] = await Promise.all([
        getProjectDashboard(projectId),
        listRecommendations(projectId).catch(() => []),
      ]);
      setDashboard(dashboardData);
      setRecommendations(recommendationData);
      setLastRefreshed(new Date().toLocaleString());
    } catch (requestError) {
      setDashboard(null);
      setRecommendations([]);
      setError(getApiErrorMessage(requestError, "Analytics could not be loaded."));
    } finally {
      setLoadingAnalytics(false);
    }
  }

  async function handleRunDemo() {
    setRunningDemo(true);
    setError(null);
    try {
      await runDemoScenario(selectedProjectId);
      await loadAnalytics(selectedProjectId);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Demo data could not be created."));
    } finally {
      setRunningDemo(false);
    }
  }

  useEffect(() => {
    void loadProjects();
  }, []);

  useEffect(() => {
    void loadAnalytics(selectedProjectId);
  }, [selectedProjectId]);

  const analyticsSummary = useMemo(() => {
    if (!dashboard) {
      return null;
    }
    const totalRuns = dashboard.overview.total_workflow_runs ?? 0;
    const totalCost = toFiniteNumber(
      dashboard.costSummary.total_cost_usd ?? dashboard.overview.total_cost_usd,
    );
    const successRate = toFiniteNumber(dashboard.outcomeSummary.success_rate);
    const costPerSuccess = toFiniteNumber(
      dashboard.outcomeSummary.cost_per_successful_outcome_usd,
    );
    const runsMissingCost = dashboard.workflowRuns.filter(
      (run) => run.total_cost_usd === null || run.total_cost_usd === undefined,
    ).length;
    const runsMissingOutcome = dashboard.workflowRuns.filter(
      (run) => !run.outcome_status,
    ).length;
    const failedRuns =
      dashboard.outcomeSummary.failed_runs || dashboard.overview.failed_runs || 0;

    return {
      totalRuns,
      totalCost,
      successRate,
      costPerSuccess,
      runsMissingCost,
      runsMissingOutcome,
      failedRuns,
    };
  }, [dashboard]);

  function exportJson() {
    if (!dashboard || !analyticsSummary) {
      return;
    }
    exportProjectSummaryAsJson(
      {
        project_name: selectedProject?.name ?? "Unknown project",
        total_runs: analyticsSummary.totalRuns,
        total_cost_usd: analyticsSummary.totalCost,
        success_rate: analyticsSummary.successRate,
        cost_per_successful_outcome_usd: analyticsSummary.costPerSuccess,
        recommendation_count: recommendations.length,
        generated_at: new Date().toISOString(),
      },
      "outcomeiq-analytics-summary.json",
    );
  }

  function exportCsv() {
    if (!dashboard || !analyticsSummary) {
      return;
    }
    exportProjectSummaryAsCsv(
      [
        {
          project_name: selectedProject?.name ?? "Unknown project",
          total_runs: analyticsSummary.totalRuns,
          total_cost_usd: analyticsSummary.totalCost ?? "",
          success_rate: analyticsSummary.successRate ?? "",
          cost_per_successful_outcome_usd: analyticsSummary.costPerSuccess ?? "",
          recommendation_count: recommendations.length,
          generated_at: new Date().toISOString(),
        },
      ],
      "outcomeiq-analytics-summary.csv",
    );
  }

  if (loadingProjects) {
    return <LoadingState message="Loading projects…" />;
  }

  if (projects.length === 0) {
    return (
      <EmptyState
        description="Create a project and run simulated demo data before reviewing analytics."
        title="No projects yet"
      />
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        description="A deeper viva-ready view of cost, outcome quality, data completeness and recommendation evidence."
        title="Analytics"
        actions={
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
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
              disabled={loadingAnalytics}
              onClick={() => void loadAnalytics(selectedProjectId)}
              type="button"
            >
              Refresh analytics
            </button>
            <button
              className="primary-button"
              disabled={runningDemo}
              onClick={() => void handleRunDemo()}
              type="button"
            >
              {runningDemo ? "Creating demo data…" : "Run Demo Data"}
            </button>
          </div>
        }
      />

      {lastRefreshed ? (
        <p className="text-xs text-slate-500">Last refreshed: {lastRefreshed}</p>
      ) : null}
      {error ? <ErrorState message={error} /> : null}
      {loadingAnalytics ? <LoadingState message="Loading analytics…" /> : null}

      {!loadingAnalytics && dashboard && analyticsSummary ? (
        <>
          <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <StatCard
              hint="Outcome-aware unit economics"
              label="Cost per successful outcome"
              tone="brand"
              value={formatUsd(analyticsSummary.costPerSuccess)}
            />
            <StatCard label="Total runs" value={analyticsSummary.totalRuns} />
            <StatCard
              label="Success rate"
              tone="emerald"
              value={formatPercent(analyticsSummary.successRate)}
            />
            <StatCard
              label="Total cost"
              value={formatUsd(analyticsSummary.totalCost)}
            />
          </section>

          <section className="grid gap-6 xl:grid-cols-2">
            <SectionCard
              description="Simple trend summary based on the currently loaded project data."
              title="Cost trend summary"
            >
              {analyticsSummary.totalRuns === 0 ? (
                <p className="text-sm text-slate-500">
                  Not enough data yet. Run demo data first.
                </p>
              ) : (
                <div className="space-y-4">
                  <MetricBar
                    label="Average cost per run"
                    max={Math.max(analyticsSummary.totalCost ?? 0, 0.0001)}
                    suffix=" USD"
                    value={
                      analyticsSummary.totalCost === null
                        ? 0
                        : analyticsSummary.totalCost / Math.max(analyticsSummary.totalRuns, 1)
                    }
                  />
                  <p className="text-sm text-slate-500">
                    Current data contains {analyticsSummary.totalRuns} run(s) and{" "}
                    {formatUsd(analyticsSummary.totalCost)} in tracked cost.
                  </p>
                </div>
              )}
            </SectionCard>

            <SectionCard title="Outcome distribution">
              <div className="space-y-4">
                <MetricBar
                  label="Successful outcomes"
                  max={Math.max(dashboard.outcomeSummary.total_runs, 1)}
                  tone="emerald"
                  value={dashboard.outcomeSummary.successful_runs}
                />
                <MetricBar
                  label="Failed outcomes"
                  max={Math.max(dashboard.outcomeSummary.total_runs, 1)}
                  tone="rose"
                  value={dashboard.outcomeSummary.failed_runs}
                />
                <MetricBar
                  label="Pending outcomes"
                  max={Math.max(dashboard.outcomeSummary.total_runs, 1)}
                  tone="amber"
                  value={dashboard.outcomeSummary.pending_runs}
                />
              </div>
            </SectionCard>
          </section>

          <SectionCard
            description="OutcomeIQ is only as useful as the evidence captured for each workflow run."
            title="Data quality summary"
            actions={
              <div className="flex flex-wrap gap-2">
                <button className="secondary-button" onClick={exportJson} type="button">
                  Export JSON
                </button>
                <button className="secondary-button" onClick={exportCsv} type="button">
                  Export CSV
                </button>
              </div>
            }
          >
            <div className="grid gap-4 md:grid-cols-3">
              <StatCard
                label="Runs missing cost"
                tone={analyticsSummary.runsMissingCost > 0 ? "amber" : "emerald"}
                value={analyticsSummary.runsMissingCost}
              />
              <StatCard
                label="Runs missing outcome"
                tone={analyticsSummary.runsMissingOutcome > 0 ? "amber" : "emerald"}
                value={analyticsSummary.runsMissingOutcome}
              />
              <StatCard
                label="Failed runs"
                tone={analyticsSummary.failedRuns > 0 ? "rose" : "emerald"}
                value={analyticsSummary.failedRuns}
              />
            </div>
          </SectionCard>
        </>
      ) : null}
    </div>
  );
}
