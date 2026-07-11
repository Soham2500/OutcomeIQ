import { type FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getApiErrorMessage } from "../api/client";
import { runDemoScenario } from "../api/demoApi";
import {
  createOrganization,
  createProject,
  listProjects,
} from "../api/projectsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { DemoScenarioSummary } from "../types/demo";
import type { Project } from "../types/project";
import { formatDateTime, shortId } from "../utils/format";

function createSlug(value: string): string {
  const base = value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);
  return `${base || "outcomeiq"}-${Date.now().toString().slice(-8)}`;
}

export function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [organizationName, setOrganizationName] = useState("");
  const [projectName, setProjectName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [runningDemoProjectId, setRunningDemoProjectId] = useState<string | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [demoSummary, setDemoSummary] = useState<DemoScenarioSummary | null>(null);

  async function refreshProjects() {
    setLoading(true);
    setError(null);
    try {
      setProjects(await listProjects());
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Projects could not be loaded."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshProjects();
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);
    setDemoSummary(null);
    try {
      const organization = await createOrganization({
        name: organizationName,
        slug: createSlug(organizationName),
      });
      const project = await createProject({
        organization_id: organization.id,
        name: projectName,
        slug: createSlug(projectName),
        description: description || undefined,
      });
      await refreshProjects();
      setOrganizationName("");
      setProjectName("");
      setDescription("");
      setSuccess(`${project.name} was created successfully.`);
    } catch (requestError) {
      const message = getApiErrorMessage(
        requestError,
        "The project could not be created.",
      );
      setError(
        message.includes("Plan limit reached")
          ? "Your plan limit is reached. Upgrade from Pricing page."
          : message,
      );
    } finally {
      setSubmitting(false);
    }
  }

  async function handleRunDemo(projectId: string) {
    setRunningDemoProjectId(projectId);
    setError(null);
    setSuccess(null);
    setDemoSummary(null);
    try {
      const summary = await runDemoScenario(projectId);
      setDemoSummary(summary);
      setSuccess("Demo scenario completed. Open the dashboard to see outcome-aware economics.");
    } catch (requestError) {
      const message = getApiErrorMessage(
        requestError,
        "Demo scenario could not run.",
      );
      setError(
        message.includes("Plan limit reached")
          ? "Monthly workflow run limit reached. Upgrade your subscription."
          : message,
      );
    } finally {
      setRunningDemoProjectId(null);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-slate-950 p-6 text-white shadow-xl md:p-8">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-brand-100">
          Project workspace
        </p>
        <h1 className="mt-2 text-2xl font-semibold">Projects</h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">
          Create the organization/project boundary, then generate simulated
          workflow data for the live demo. Each project owns its workflows, costs,
          outcomes and recommendations.
        </p>
      </div>

      <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-card md:p-6">
        <h2 className="font-semibold text-slate-900">Create a project</h2>
        <p className="mt-1 text-sm text-slate-500">
          Keep organization, project name and description separate so the portfolio
          demo stays clean and explainable.
        </p>
        {error ? (
          <div className="mt-4">
            <ErrorState message={error} />
          </div>
        ) : null}
        {success ? (
          <p className="mt-4 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
            {success}
          </p>
        ) : null}
        {demoSummary ? (
          <div className="mt-4 rounded-lg border border-brand-100 bg-brand-50 p-4 text-sm text-brand-900">
            <p className="font-semibold">{demoSummary.message}</p>
            <p className="mt-2 font-mono text-xs">
              Workflow {shortId(demoSummary.workflow_id)} · Runs{" "}
              {shortId(demoSummary.run_a_id)}, {shortId(demoSummary.run_b_id)}
            </p>
          </div>
        ) : null}
        <form className="mt-5 grid gap-4 md:grid-cols-2" onSubmit={handleCreate}>
          <label>
            <span className="field-label">Organization name</span>
            <input
              className="field-input"
              onChange={(event) => setOrganizationName(event.target.value)}
              placeholder="Example AI Operations"
              required
              value={organizationName}
            />
          </label>
          <label>
            <span className="field-label">Project name</span>
            <input
              className="field-input"
              onChange={(event) => setProjectName(event.target.value)}
              placeholder="Customer Support AI"
              required
              value={projectName}
            />
          </label>
          <label className="md:col-span-2">
            <span className="field-label">Description</span>
            <textarea
              className="field-input min-h-24 resize-y"
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Outcome-aware support workflow evaluation"
              value={description}
            />
          </label>
          <div className="md:col-span-2">
            <button className="primary-button" disabled={submitting} type="submit">
              {submitting ? "Creating…" : "Create organization and project"}
            </button>
          </div>
        </form>
      </section>

      <section>
        <h2 className="mb-4 font-semibold text-slate-900">Your projects</h2>
        {loading ? <LoadingState message="Loading projects…" /> : null}
        {!loading && projects.length === 0 ? (
          <EmptyState
            description="Use the form above to create the first project boundary."
            title="No projects available"
          />
        ) : null}
        {!loading && projects.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {projects.map((project) => (
              <article
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-card transition hover:-translate-y-0.5 hover:border-brand-100 hover:shadow-md"
                key={project.id}
              >
                <div className="flex items-start justify-between gap-3">
                  <h3 className="font-semibold text-slate-900">{project.name}</h3>
                  <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium capitalize text-emerald-700">
                    {project.status}
                  </span>
                </div>
                <p className="mt-3 line-clamp-2 text-sm text-slate-500">
                  {project.description || "No project description provided."}
                </p>
                <div className="mt-4 space-y-1 text-xs text-slate-400">
                  <p>Created · {formatDateTime(project.created_at)}</p>
                  <p className="font-mono">
                  Project ID · {shortId(project.id)}
                  </p>
                </div>
                <div className="mt-5 flex flex-wrap gap-2">
                  <Link className="secondary-button" to="/dashboard">
                    Open Dashboard
                  </Link>
                  <Link className="secondary-button" to="/analytics">
                    Open Analytics
                  </Link>
                  <button
                    className="primary-button"
                    disabled={runningDemoProjectId === project.id}
                    onClick={() => void handleRunDemo(project.id)}
                    type="button"
                  >
                    {runningDemoProjectId === project.id
                      ? "Running demo…"
                      : "Run Demo Scenario"}
                  </button>
                  <Link className="secondary-button" to="/recommendations">
                    Open Recommendations
                  </Link>
                </div>
              </article>
            ))}
          </div>
        ) : null}
      </section>
    </div>
  );
}
