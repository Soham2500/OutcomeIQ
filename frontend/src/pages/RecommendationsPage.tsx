import { useEffect, useState } from "react";
import { getApiErrorMessage } from "../api/client";
import { listProjects } from "../api/projectsApi";
import {
  generateRecommendations,
  listRecommendations,
  updateRecommendationStatus,
} from "../api/recommendationsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { Project } from "../types/project";
import type {
  Recommendation,
  RecommendationSeverity,
} from "../types/recommendation";
import { formatUsd } from "../utils/format";

const severityClasses: Record<RecommendationSeverity, string> = {
  low: "bg-sky-50 text-sky-700",
  medium: "bg-amber-50 text-amber-700",
  high: "bg-rose-50 text-rose-700",
};

const statusClasses: Record<string, string> = {
  open: "bg-violet-50 text-violet-700",
  accepted: "bg-emerald-50 text-emerald-700",
  dismissed: "bg-slate-100 text-slate-600",
  resolved: "bg-blue-50 text-blue-700",
};

export function RecommendationsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [dismissingId, setDismissingId] = useState<string | null>(null);
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
      setRecommendations([]);
      return;
    }
    let active = true;
    setLoadingRecommendations(true);
    setError(null);
    listRecommendations(selectedProjectId)
      .then((items) => {
        if (active) {
          setRecommendations(items);
        }
      })
      .catch((requestError: unknown) => {
        if (active) {
          setError(
            getApiErrorMessage(requestError, "Recommendations could not be loaded."),
          );
        }
      })
      .finally(() => {
        if (active) {
          setLoadingRecommendations(false);
        }
      });
    return () => {
      active = false;
    };
  }, [selectedProjectId]);

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    try {
      await generateRecommendations(selectedProjectId);
      setRecommendations(await listRecommendations(selectedProjectId));
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

  if (error && projects.length === 0) {
    return <ErrorState message={error} onRetry={() => void loadProjectOptions()} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Recommendations</h1>
          <p className="mt-1 text-sm text-slate-500">
            Rule-based MVP suggestions backed by cost and outcome evidence. They do
            not automatically change workflows.
          </p>
        </div>
        {projects.length > 0 ? (
          <div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row sm:items-end">
            <label className="w-full sm:w-64">
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
              className="primary-button whitespace-nowrap"
              disabled={generating || !selectedProjectId}
              onClick={() => void handleGenerate()}
              type="button"
            >
              {generating ? "Generating…" : "Generate recommendations"}
            </button>
          </div>
        ) : null}
      </div>

      {error ? <ErrorState message={error} /> : null}
      {projects.length === 0 ? (
        <EmptyState
          description="Create a project before generating evidence-backed recommendations."
          title="No project available"
        />
      ) : null}
      {loadingRecommendations ? (
        <LoadingState message="Loading recommendations…" />
      ) : null}
      {!loadingRecommendations && projects.length > 0 && recommendations.length === 0 ? (
        <EmptyState
          description="Generate recommendations after workflow runs, costs and outcomes have been recorded."
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
                    <span
                      className={`rounded-full px-2.5 py-1 text-xs font-semibold capitalize ${severityClasses[recommendation.severity]}`}
                    >
                      {recommendation.severity}
                    </span>
                    <span
                      className={`rounded-full px-2.5 py-1 text-xs font-medium capitalize ${statusClasses[recommendation.status] ?? statusClasses.open}`}
                    >
                      {recommendation.status}
                    </span>
                    <span className="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-medium capitalize text-brand-700">
                      {recommendation.recommendation_type.replaceAll("_", " ")}
                    </span>
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
