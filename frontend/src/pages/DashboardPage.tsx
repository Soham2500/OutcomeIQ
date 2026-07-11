import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../api/client";
import { getMyBilling, type MyBilling } from "../api/billingApi";
import { getProjectDashboard } from "../api/dashboardApi";
import { runDemoScenario } from "../api/demoApi";
import { listProjects } from "../api/projectsApi";
import { listRecommendations } from "../api/recommendationsApi";
import { Badge } from "../components/Badge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
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
import {
  formatDateTime,
  formatPercent,
  formatUsd,
  shortId,
  toFiniteNumber,
} from "../utils/format";

function statusTone(status?: string | null) {
  if (status === "succeeded") {
    return "emerald";
  }
  if (status === "failed" || status === "cancelled") {
    return "rose";
  }
  if (status === "running" || status === "pending") {
    return "amber";
  }
  return "slate";
}

export function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [billing, setBilling] = useState<MyBilling | null>(null);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [lastRefreshed, setLastRefreshed] = useState<string | null>(null);

  const selectedProject = projects.find((project) => project.id === selectedProjectId);

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
      setRecommendations([]);
      return;
    }
    setLoadingDashboard(true);
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
      const message = getApiErrorMessage(
        requestError,
        "Demo data could not be created.",
      );
      setError(
        message.includes("Plan limit reached")
          ? "Monthly workflow run limit reached. Upgrade your subscription."
          : message,
      );
    } finally {
      setRunningDemo(false);
    }
  }

  useEffect(() => {
    void loadProjectOptions();
  }, []);

  useEffect(() => {
    let active = true;
    getMyBilling()
      .then((billingData) => {
        if (active) {
          setBilling(billingData);
        }
      })
      .catch(() => {
        if (active) {
          setBilling(null);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    void loadDashboard(selectedProjectId);
  }, [selectedProjectId]);

  const summary = useMemo(() => {
    if (!dashboard) {
      return null;
    }
    const totalRuns = dashboard.overview.total_workflow_runs ?? 0;
    const totalCost = toFiniteNumber(
      dashboard.costSummary.total_cost_usd ?? dashboard.overview.total_cost_usd,
    );
    const averageCostPerRun =
      totalCost === null || totalRuns === 0 ? null : totalCost / totalRuns;
    const successRate = toFiniteNumber(dashboard.outcomeSummary.success_rate);
    const costPerSuccess = toFiniteNumber(
      dashboard.outcomeSummary.cost_per_successful_outcome_usd,
    );
    const missingOutcomes = dashboard.workflowRuns.filter(
      (run) => !run.outcome_status,
    ).length;

    return {
      totalRuns,
      totalCost,
      averageCostPerRun,
      successRate,
      costPerSuccess,
      missingOutcomes,
    };
  }, [dashboard]);

  const insights = useMemo(() => {
    if (!dashboard || !summary || summary.totalRuns === 0) {
      return [];
    }
    const items: Array<{ title: string; detail: string; tone: "brand" | "amber" | "rose" }> = [];
    if (
      summary.costPerSuccess !== null &&
      summary.averageCostPerRun !== null &&
      summary.costPerSuccess > summary.averageCostPerRun
    ) {
      items.push({
        title: "Cheapest request is not always cheapest outcome",
        detail:
          "Cost per successful outcome is higher than average cost per run because not every run succeeds.",
        tone: "brand",
      });
    }
    if (summary.missingOutcomes > 0) {
      items.push({
        title: "Missing outcomes reduce decision quality",
        detail: `${summary.missingOutcomes} run(s) do not yet have verified outcome evidence.`,
        tone: "amber",
      });
    }
    if (dashboard.outcomeSummary.failed_runs > 0) {
      items.push({
        title: "Failed outcomes increase effective cost",
        detail: `${dashboard.outcomeSummary.failed_runs} failed outcome(s) are included in spend but not in successful yield.`,
        tone: "rose",
      });
    }
    return items;
  }, [dashboard, summary]);

  function exportJson() {
    if (!dashboard || !summary) {
      return;
    }
    exportProjectSummaryAsJson(
      {
        project_name: selectedProject?.name ?? "Unknown project",
        total_runs: summary.totalRuns,
        total_cost_usd: summary.totalCost,
        success_rate: summary.successRate,
        cost_per_successful_outcome_usd: summary.costPerSuccess,
        recommendation_count: recommendations.length,
        generated_at: new Date().toISOString(),
      },
      "outcomeiq-dashboard-summary.json",
    );
  }

  function exportCsv() {
    if (!dashboard || !summary) {
      return;
    }
    exportProjectSummaryAsCsv(
      [
        {
          project_name: selectedProject?.name ?? "Unknown project",
          total_runs: summary.totalRuns,
          total_cost_usd: summary.totalCost ?? "",
          success_rate: summary.successRate ?? "",
          cost_per_successful_outcome_usd: summary.costPerSuccess ?? "",
          recommendation_count: recommendations.length,
          generated_at: new Date().toISOString(),
        },
      ],
      "outcomeiq-dashboard-summary.csv",
    );
  }

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
      <PageHeader
        description="Executive view of workflow cost, outcome quality and business-unit economics."
        title="Dashboard"
        actions={
          <div className="flex flex-col gap-3 lg:flex-row lg:items-end">
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
        }
      />

      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-xs text-slate-500">
          Last refreshed: {lastRefreshed ?? "Not refreshed yet"}
        </p>
        <div className="flex flex-wrap gap-2">
          <button
            className="secondary-button"
            disabled={!dashboard}
            onClick={exportJson}
            type="button"
          >
            Export JSON
          </button>
          <button
            className="secondary-button"
            disabled={!dashboard}
            onClick={exportCsv}
            type="button"
          >
            Export CSV
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

      {!loadingDashboard && dashboard && summary ? (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard label="Total workflow runs" value={summary.totalRuns} />
            <StatCard
              label="Total cost USD"
              value={formatUsd(summary.totalCost)}
            />
            <StatCard
              label="Successful outcomes"
              tone="emerald"
              value={dashboard.outcomeSummary.successful_runs}
            />
            <StatCard
              label="Failed outcomes"
              tone={dashboard.outcomeSummary.failed_runs > 0 ? "rose" : "default"}
              value={dashboard.outcomeSummary.failed_runs}
            />
            <StatCard
              label="Success rate"
              tone="emerald"
              value={formatPercent(summary.successRate)}
            />
            <StatCard
              hint="Outcome-aware unit economics"
              label="Cost per successful outcome"
              tone="brand"
              value={formatUsd(summary.costPerSuccess)}
            />
            <StatCard
              label="Average cost per run"
              value={formatUsd(summary.averageCostPerRun)}
            />
            <StatCard
              hint="Not available until outcome value is captured"
              label="Total business value"
              value="Not enough data"
            />
          </section>

          <SectionCard tone="brand">
            <p className="text-sm font-semibold text-brand-950">
              OutcomeIQ focuses on cost per successful business outcome, not only
              cost per AI request.
            </p>
            <p className="mt-2 text-sm leading-6 text-brand-900">
              This is why a workflow with a low request cost can still be a poor
              business decision if many runs fail, escalate or lack verified
              outcome evidence.
            </p>
          </SectionCard>

          {billing ? (
            <SectionCard
              description={`${billing.usage.projects_used}/${billing.usage.max_projects} projects · ${billing.usage.workflow_runs_used}/${billing.usage.max_workflow_runs_per_month} workflow runs this month`}
              title={`Plan: ${billing.plan.name}`}
            >
              <p className="text-sm text-slate-600">
                Billing is in {billing.payment_mode} mode. Backend plan limits
                control project creation and workflow-run usage.
              </p>
            </SectionCard>
          ) : null}

          {insights.length > 0 ? (
            <section className="grid gap-4 lg:grid-cols-3">
              {insights.map((insight) => (
                <SectionCard key={insight.title} tone={insight.tone === "brand" ? "brand" : "default"}>
                  <div className="flex items-start gap-3">
                    <Badge tone={insight.tone}>{insight.tone}</Badge>
                    <div>
                      <h2 className="font-semibold text-slate-900">{insight.title}</h2>
                      <p className="mt-2 text-sm leading-6 text-slate-600">
                        {insight.detail}
                      </p>
                    </div>
                  </div>
                </SectionCard>
              ))}
            </section>
          ) : null}

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
                  description="No workflow runs yet. Demo data uses simulated AI model/tool calls and does not require real provider keys."
                  title="No workflow runs yet"
                />
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
                  <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="px-5 py-3 font-medium">Run</th>
                      <th className="px-5 py-3 font-medium">Workflow</th>
                      <th className="px-5 py-3 font-medium">Status</th>
                      <th className="px-5 py-3 font-medium">Cost</th>
                      <th className="px-5 py-3 font-medium">Outcome</th>
                      <th className="px-5 py-3 font-medium">Started</th>
                      <th className="px-5 py-3 font-medium">Completed</th>
                      <th className="px-5 py-3 font-medium">Action</th>
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
                        <td className="whitespace-nowrap px-5 py-3 text-slate-700">
                          {run.workflow_name ?? shortId(run.workflow_id)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3">
                          <Badge tone={statusTone(run.status)}>
                            {(run.status || "unknown").replaceAll("_", " ")}
                          </Badge>
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-slate-700">
                          {formatUsd(run.total_cost_usd)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3">
                          <Badge tone={statusTone(run.outcome_status)}>
                            {run.outcome_status?.replaceAll("_", " ") ??
                              "Pending evidence"}
                          </Badge>
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDateTime(run.started_at)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {formatDateTime(run.completed_at)}
                        </td>
                        <td className="whitespace-nowrap px-5 py-3 text-xs text-slate-500">
                          {run.workflow_run_id ? "Trace available via API" : "—"}
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
