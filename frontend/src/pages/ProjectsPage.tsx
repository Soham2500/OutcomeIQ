import { type FormEvent, useEffect, useState } from "react";
import { getApiErrorMessage } from "../api/client";
import {
  createOrganization,
  createProject,
  listProjects,
} from "../api/projectsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { Project } from "../types/project";
import { shortId } from "../utils/format";

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
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

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
      setProjects((current) => [project, ...current]);
      setOrganizationName("");
      setProjectName("");
      setDescription("");
      setSuccess(`${project.name} was created successfully.`);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "The project could not be created."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Projects</h1>
        <p className="mt-1 text-sm text-slate-500">
          Projects group workflows, costs, outcomes, and recommendations.
        </p>
      </div>

      <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-card md:p-6">
        <h2 className="font-semibold text-slate-900">Create a project</h2>
        <p className="mt-1 text-sm text-slate-500">
          Create an organization boundary first, then place the AI workflow project inside it.
        </p>
        {error ? <div className="mt-4"><ErrorState message={error} /></div> : null}
        {success ? (
          <p className="mt-4 rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
            {success}
          </p>
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
                <p className="mt-4 font-mono text-xs text-slate-400">
                  Project ID · {shortId(project.id)}
                </p>
              </article>
            ))}
          </div>
        ) : null}
      </section>
    </div>
  );
}
