import { type FormEvent, useEffect, useState } from "react";
import { getApiErrorMessage } from "../api/client";
import { runDemoScenario } from "../api/demoApi";
import { listProjects } from "../api/projectsApi";
import { createWorkflow, listWorkflows } from "../api/workflowsApi";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import type { DemoScenarioSummary } from "../types/demo";
import type { Project } from "../types/project";
import type { Workflow } from "../types/workflow";
import { shortId } from "../utils/format";

function createSlug(value: string): string {
  const base = value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);
  return `${base || "workflow"}-${Date.now().toString().slice(-8)}`;
}

export function WorkflowsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState("");
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [workflowName, setWorkflowName] = useState("Support Ticket Classifier");
  const [description, setDescription] = useState(
    "Simulated customer-support workflow for outcome-aware FinOps analysis.",
  );
  const [loadingProjects, setLoadingProjects] = useState(true);
  const [loadingWorkflows, setLoadingWorkflows] = useState(false);
  const [creating, setCreating] = useState(false);
  const [runningDemo, setRunningDemo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [demoSummary, setDemoSummary] = useState<DemoScenarioSummary | null>(null);

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

  async function loadWorkflows(projectId: string) {
    if (!projectId) {
      setWorkflows([]);
      return;
    }
    setLoadingWorkflows(true);
    setError(null);
    try {
      setWorkflows(await listWorkflows(projectId));
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Workflows could not be loaded."));
    } finally {
      setLoadingWorkflows(false);
    }
  }

  useEffect(() => {
    void loadProjects();
  }, []);

  useEffect(() => {
    void loadWorkflows(selectedProjectId);
  }, [selectedProjectId]);

  async function handleCreateWorkflow(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCreating(true);
    setError(null);
    setSuccess(null);
    setDemoSummary(null);
    try {
      const workflow = await createWorkflow({
        project_id: selectedProjectId,
        name: workflowName,
        slug: createSlug(workflowName),
        description: description || undefined,
      });
      setSuccess(`${workflow.name} was created.`);
      setWorkflowName("Support Ticket Classifier");
      setDescription(
        "Simulated customer-support workflow for outcome-aware FinOps analysis.",
      );
      await loadWorkflows(selectedProjectId);
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, "Workflow could not be created."));
    } finally {
      setCreating(false);
    }
  }

  async function handleRunDemo() {
    setRunningDemo(true);
    setError(null);
    setSuccess(null);
    setDemoSummary(null);
    try {
      const summary = await runDemoScenario(selectedProjectId);
      setDemoSummary(summary);
      setSuccess("Simulated workflow runs, costs and outcomes were recorded.");
      await loadWorkflows(selectedProjectId);
    } catch (requestError) {
      const message = getApiErrorMessage(
        requestError,
        "Demo workflow could not run.",
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

  if (loadingProjects) {
    return <LoadingState message="Loading projects…" />;
  }

  if (projects.length === 0) {
    return (
      <EmptyState
        description="Create a project before registering workflows or running simulated workflow data."
        title="No projects yet"
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Workflows</h1>
          <p className="mt-1 text-sm text-slate-500">
            Register support workflows and run a simulated ticket-resolution trace
            without opening Swagger.
          </p>
        </div>
        <label className="w-full lg:w-80">
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
      {success ? (
        <p className="rounded-lg bg-emerald-50 p-3 text-sm text-emerald-700">
          {success}
        </p>
      ) : null}
      {demoSummary ? (
        <section className="rounded-xl border border-brand-100 bg-brand-50 p-5">
          <h2 className="font-semibold text-brand-950">Demo run summary</h2>
          <p className="mt-2 text-sm text-brand-900">{demoSummary.message}</p>
          <div className="mt-3 grid gap-2 font-mono text-xs text-brand-900 sm:grid-cols-3">
            <span>Workflow: {shortId(demoSummary.workflow_id)}</span>
            <span>Run A: {shortId(demoSummary.run_a_id)}</span>
            <span>Run B: {shortId(demoSummary.run_b_id)}</span>
          </div>
        </section>
      ) : null}

      <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
        <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-card md:p-6">
          <h2 className="font-semibold text-slate-900">Create workflow</h2>
          <form className="mt-5 space-y-4" onSubmit={handleCreateWorkflow}>
            <label>
              <span className="field-label">Workflow name</span>
              <input
                className="field-input"
                onChange={(event) => setWorkflowName(event.target.value)}
                required
                value={workflowName}
              />
            </label>
            <label>
              <span className="field-label">Description</span>
              <textarea
                className="field-input min-h-24 resize-y"
                onChange={(event) => setDescription(event.target.value)}
                value={description}
              />
            </label>
            <div className="flex flex-wrap gap-3">
              <button
                className="secondary-button"
                disabled={creating || !selectedProjectId}
                type="submit"
              >
                {creating ? "Creating…" : "Create Workflow"}
              </button>
              <button
                className="primary-button"
                disabled={runningDemo || !selectedProjectId}
                onClick={() => void handleRunDemo()}
                type="button"
              >
                {runningDemo ? "Running simulated workflow…" : "Run Simulated Workflow"}
              </button>
            </div>
          </form>
        </article>

        <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-card md:p-6">
          <h2 className="font-semibold text-slate-900">Registered workflows</h2>
          {loadingWorkflows ? (
            <div className="mt-4">
              <LoadingState message="Loading workflows…" />
            </div>
          ) : null}
          {!loadingWorkflows && workflows.length === 0 ? (
            <div className="mt-4">
              <EmptyState
                description="Create a workflow manually or run the simulated support workflow demo."
                title="No workflows yet"
              />
            </div>
          ) : null}
          {!loadingWorkflows && workflows.length > 0 ? (
            <div className="mt-4 space-y-3">
              {workflows.map((workflow) => (
                <div
                  className="rounded-lg border border-slate-200 p-4"
                  key={workflow.id}
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold text-slate-900">
                        {workflow.name}
                      </h3>
                      <p className="mt-1 text-sm text-slate-500">
                        {workflow.description || "No description provided."}
                      </p>
                    </div>
                    <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">
                      {workflow.status}
                    </span>
                  </div>
                  <p className="mt-3 font-mono text-xs text-slate-400">
                    Workflow ID · {shortId(workflow.id)}
                  </p>
                </div>
              ))}
            </div>
          ) : null}
        </article>
      </section>
    </div>
  );
}
