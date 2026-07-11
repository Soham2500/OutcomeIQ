import { useEffect, useState } from "react";
import { getApiErrorMessage } from "../api/client";
import { runDemoScenario } from "../api/demoApi";
import { listProjects } from "../api/projectsApi";
import {
  generateRecommendations,
  listRecommendations,
  updateRecommendationStatus,
} from "../api/recommendationsApi";
import { Badge } from "../components/Badge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { Project } from "../types/project";
import type {
  Recommendation,
  RecommendationSeverity,
  RecommendationStatus,
} from "../types/recommendation";
import { formatUsd } from "../utils/format";

const severityTone: Record<RecommendationSeverity, "sky" | "amber" | "rose"> = {
  low: "sky",
  medium: "amber",
  high: "rose",
};

const statusTone: Record<
  RecommendationStatus,
  "violet" | "emerald" | "slate" | "sky"
> = {
  open: "violet",
  accepted: "emerald",
  dismissed: "slate",
  resolved: "sky",
};

export function RecommendationsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [dismissingId, setDismissingId] = useState<string | null>(null);
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

  async function loadRecommendations(projectId: string) {
    if (!projectId) {
      setRecommendations([]);
      return;
    }
    setLoadingRecommendations(true);
    setError(null);
    try {
      setRecommendations(await listRecommendations(projectId));
    } catch (requestError) {
      setError(
        getApiErrorMessage(requestError, "Recommendations could not be loaded."),
      );
    } finally {
      setLoadingRecommendations(false);
    }
  }

  useEffect(() => {
    void loadProjectOptions();
  }, []);

  useEffect(() => {
    void loadRecommendations(selectedProjectId);
  }, [selectedProjectId]);

  async function handleRunDemo() {
    setRunningDemo(true);
    setError(null);
    setSuccess(null);
    try {
      await runDemoScenario(selectedProjectId);
      setSuccess("Demo data created. Generate recommendations to review evidence-backed actions.");
      await loadRecommendations(selectedProjectId);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Demo data could not be created."));
    } finally {
      setRunningDemo(false);
    }
  }

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    setSuccess(null);
    try {
      const generated = await generateRecommendations(selectedProjectId);
      setRecommendations(await listRecommendations(selectedProjectId));
      setSuccess(
        generated.generated_count > 0
          ? `${generated.generated_count} recommendation(s) generated.`
          : "No new recommendations were generated for the current evidence.",
      );
    } catch (requestError) {
      setError(
        getApiErrorMessage(requestError, "Recommendations could not be generated."),
      );
    } finally {
      setGenerating(false);
    }
  }

  async function handleDismiss(recommendationId: string) {
    setDismissingId(recommendationId);
    setError(null);
    try {
      const updated = await updateRecommendationStatus(
        recommendationId,
        "dismissed",
      );
      setRecommendations((current) =>
        current.map((item) => (item.id === updated.id ? updated : item)),
      );
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Recommendation could not be dismissed."));
    } finally {
      setDismissingId(null);
    }
  }

  if (loadingProjects) {
    return <LoadingState message="Loading projects…" />;
  }

  if (projects.length === 0) {
    return (
      <EmptyState
        description="Create a project and run demo data before generating recommendations."
        title="No projects yet"
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">
            Recommendations
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Evidence-backed actions for cost, failure waste and outcome quality.
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
            disabled={runningDemo || !selectedProjectId}
            onClick={() => void handleRunDemo()}
            type="button"
          >
            {runningDemo ? "Creating demo data…" : "Run Demo Data"}
          </button>
          <button
            className="primary-button"
            disabled={generating || !selectedProjectId}
            onClick={() => void handleGenerate()}
            type="button"
          >
            {generating ? "Generating…" : "Generate Recommendations"}
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
          onRetry={() => void loadRecommendations(selectedProjectId)}
        />
      ) : null}
      {loadingRecommendations ? (
        <LoadingState message="Loading recommendations…" />
      ) : null}

      {!loadingRecommendations && recommendations.length === 0 ? (
        <EmptyState
          action={
            <div className="flex flex-wrap justify-center gap-3">
              <button
                className="secondary-button"
                disabled={runningDemo}
                onClick={() => void handleRunDemo()}
                type="button"
              >
                {runningDemo ? "Creating demo data…" : "Run demo data first"}
              </button>
              <button
                className="primary-button"
                disabled={generating}
                onClick={() => void handleGenerate()}
                type="button"
              >
                {generating ? "Generating…" : "Generate recommendations"}
              </button>
            </div>
          }
          description="Run demo data first, then generate recommendations."
          title="No recommendations yet"
        />
      ) : null}

      {!loadingRecommendations && recommendations.length > 0 ? (
        <div className="space-y-4">
          {recommendations.map((recommendation) => (
            <article
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-card"
              key={recommendation.id}
            >
              <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge tone={severityTone[recommendation.severity]}>
                      {recommendation.severity}
                    </Badge>
                    <Badge tone={statusTone[recommendation.status]}>
                      {recommendation.status}
                    </Badge>
                    <Badge tone="brand">
                      {recommendation.recommendation_type.replaceAll("_", " ")}
                    </Badge>
                  </div>
                  <h2 className="mt-3 font-semibold text-slate-900">
                    {recommendation.title}
                  </h2>
                  {recommendation.description ? (
                    <p className="mt-2 max-w-3xl text-sm text-slate-600">
                      {recommendation.description}
                    </p>
                  ) : null}
                  {recommendation.potential_savings_usd !== null ? (
                    <p className="mt-3 text-sm font-medium text-emerald-700">
                      Potential savings: {formatUsd(recommendation.potential_savings_usd)}
                    </p>
                  ) : null}
                </div>
                {recommendation.status === "open" ? (
                  <button
                    className="secondary-button shrink-0"
                    disabled={dismissingId === recommendation.id}
                    onClick={() => void handleDismiss(recommendation.id)}
                    type="button"
                  >
                    {dismissingId === recommendation.id ? "Dismissing…" : "Dismiss"}
                  </button>
                ) : null}
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </div>
  );
}
