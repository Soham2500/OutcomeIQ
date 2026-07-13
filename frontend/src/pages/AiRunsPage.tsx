import { type FormEvent, useEffect, useMemo, useState } from "react";
import { Copy, Cpu, Sparkles, Zap } from "lucide-react";
import { createAiRun, listAiRuns } from "../api/aiRunsApi";
import { getApiErrorMessage } from "../api/client";
import { listProjects } from "../api/projectsApi";
import { Badge } from "../components/Badge";
import { EmptyState } from "../components/EmptyState";
import { PageHeader } from "../components/PageHeader";
import { SectionCard } from "../components/SectionCard";
import { SkeletonCard } from "../components/SkeletonCard";
import { useToast } from "../components/Toast";
import type { AiProvider, AiRun } from "../types/aiRun";
import type { Project } from "../types/project";

const providerDefaults: Record<AiProvider, string> = {
  gemini: "gemini-2.5-flash",
  openai: "gpt-4o-mini",
};

function formatInr(value: string | number): string {
  const amount = Number(value);
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 6,
  }).format(Number.isFinite(amount) ? amount : 0);
}

export function AiRunsPage() {
  const { notify } = useToast();
  const [projects, setProjects] = useState<Project[]>([]);
  const [projectId, setProjectId] = useState("");
  const [workflowName, setWorkflowName] = useState("AI Test Run");
  const [provider, setProvider] = useState<AiProvider>("gemini");
  const [model, setModel] = useState(providerDefaults.gemini);
  const [prompt, setPrompt] = useState("");
  const [runs, setRuns] = useState<AiRun[]>([]);
  const [latestRun, setLatestRun] = useState<AiRun | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    async function loadInitialData() {
      setLoading(true);
      setError(null);
      try {
        const [projectList, runList] = await Promise.all([
          listProjects(),
          listAiRuns(),
        ]);
        if (!isMounted) {
          return;
        }
        setProjects(projectList);
        setRuns(runList);
        if (projectList[0]) {
          setProjectId(projectList[0].id);
        }
      } catch (requestError) {
        if (isMounted) {
          setError(getApiErrorMessage(requestError, "Could not load AI runs."));
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }
    void loadInitialData();
    return () => {
      isMounted = false;
    };
  }, []);

  const filteredRuns = useMemo(
    () => runs.filter((run) => !projectId || run.project_id === projectId),
    [runs, projectId],
  );

  function handleProviderChange(nextProvider: AiProvider) {
    setProvider(nextProvider);
    setModel(providerDefaults[nextProvider]);
  }

  async function refreshRuns(selectedProjectId = projectId) {
    const runList = await listAiRuns(selectedProjectId || undefined);
    setRuns((currentRuns) => {
      const otherRuns = currentRuns.filter(
        (run) => selectedProjectId && run.project_id !== selectedProjectId,
      );
      return selectedProjectId ? [...runList, ...otherRuns] : runList;
    });
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setLatestRun(null);
    try {
      const run = await createAiRun({
        project_id: projectId,
        workflow_name: workflowName,
        prompt,
        provider,
        model: model.trim() || undefined,
      });
      setLatestRun(run);
      notify({
        tone: run.status === "succeeded" ? "success" : "warning",
        title: run.status === "succeeded" ? "AI run completed" : "AI run recorded",
        description: `${run.provider} · ${run.total_tokens.toLocaleString("en-IN")} tokens · ${formatInr(run.cost_inr)}`,
      });
      await refreshRuns(projectId);
    } catch (requestError) {
      const message = getApiErrorMessage(requestError, "AI run failed.");
      setError(message);
      notify({ tone: "error", title: "AI run failed", description: message });
    } finally {
      setSubmitting(false);
    }
  }

  async function copyLatestResponse() {
    if (!latestRun?.response_text) {
      return;
    }
    await navigator.clipboard.writeText(latestRun.response_text);
    notify({ tone: "success", title: "Response copied" });
  }

  return (
    <div className="space-y-6">
      <PageHeader
        description="Run a backend-only Gemini or OpenAI test, track tokens, latency and INR cost, and keep provider keys away from the browser."
        eyebrow="Real AI usage"
        title="Run AI Test"
      />

      {loading ? (
        <section className="grid gap-4 md:grid-cols-3">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </section>
      ) : null}

      {error ? (
        <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      <SectionCard
        description="Prompt text is sent from the backend to the selected provider. OutcomeIQ stores previews, tokens, cost and status."
        title="Create AI run"
      >
        <form className="grid gap-5 lg:grid-cols-2" onSubmit={handleSubmit}>
          <label>
            <span className="field-label">Project</span>
            <select
              className="field-input"
              disabled={loading || projects.length === 0}
              onChange={(event) => setProjectId(event.target.value)}
              required
              value={projectId}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            <span className="field-label">Workflow name</span>
            <input
              className="field-input"
              maxLength={160}
              onChange={(event) => setWorkflowName(event.target.value)}
              required
              value={workflowName}
            />
          </label>
          <label>
            <span className="field-label">Provider</span>
            <div className="grid grid-cols-2 gap-3">
              {(["gemini", "openai"] as AiProvider[]).map((item) => (
                <button
                  className={`rounded-2xl border px-4 py-3 text-left text-sm font-semibold transition ${
                    provider === item
                      ? "border-brand-300 bg-brand-50 text-brand-800 ring-2 ring-brand-100"
                      : "border-slate-200 bg-white/80 text-slate-600 hover:border-brand-200"
                  }`}
                  key={item}
                  onClick={() => handleProviderChange(item)}
                  type="button"
                >
                  <span className="flex items-center gap-2">
                    {item === "gemini" ? <Sparkles className="h-4 w-4" /> : <Cpu className="h-4 w-4" />}
                    {item === "gemini" ? "Gemini" : "OpenAI"}
                  </span>
                </button>
              ))}
            </div>
          </label>
          <label>
            <span className="field-label">Model</span>
            <input
              className="field-input"
              onChange={(event) => setModel(event.target.value)}
              placeholder={providerDefaults[provider]}
              value={model}
            />
          </label>
          <label className="lg:col-span-2">
            <span className="field-label">Prompt</span>
            <textarea
              className="field-input min-h-40"
              maxLength={8000}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="Ask the selected model to summarize a synthetic workflow, draft a test analysis, or classify demo support data."
              required
              value={prompt}
            />
            <span className="mt-1 block text-xs text-slate-500">
              {prompt.length}/8000 characters
            </span>
          </label>
          <div className="lg:col-span-2">
            <button
              className="primary-button"
              disabled={submitting || !projectId}
              type="submit"
            >
              <Zap aria-hidden="true" className="h-4 w-4" />
              {submitting ? "Running AI test…" : "Run AI Test"}
            </button>
          </div>
        </form>
      </SectionCard>

      {latestRun ? (
        <SectionCard
          title="Latest response"
          actions={
            latestRun.response_text ? (
              <button className="secondary-button" onClick={() => void copyLatestResponse()} type="button">
                <Copy aria-hidden="true" className="h-4 w-4" />
                Copy response
              </button>
            ) : null
          }
        >
          <div className="grid gap-3 text-sm md:grid-cols-3">
            <Metric label="Provider" value={providerLabel(latestRun.provider)} />
            <Metric label="Model" value={latestRun.model} />
            <Metric label="Latency" value={`${latestRun.latency_ms} ms`} />
            <Metric label="Input tokens" value={latestRun.input_tokens} />
            <Metric label="Output tokens" value={latestRun.output_tokens} />
            <Metric label="Total tokens" value={latestRun.total_tokens} />
            <Metric label="Cost" value={formatInr(latestRun.cost_inr)} />
            <Metric
              label="Pricing"
              value={latestRun.pricing_unknown ? "Unknown" : "Mapped"}
            />
            <Metric label="Status" value={latestRun.status} />
          </div>
          {latestRun.status === "failed" ? (
            <p className="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-amber-700">
              {latestRun.error_message}
            </p>
          ) : (
            <pre className="mt-4 whitespace-pre-wrap rounded-xl bg-slate-950 p-4 text-sm leading-6 text-slate-50">
              {latestRun.response_text}
            </pre>
          )}
        </SectionCard>
      ) : null}

      <SectionCard title="Latest AI runs">
        {filteredRuns.length === 0 ? (
          <EmptyState
            description="Create a backend-only Gemini or OpenAI run to see tokens, latency, INR cost and safe response previews."
            title="No AI runs yet"
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
              <thead className="text-left text-xs uppercase tracking-wider text-slate-500">
                <tr>
                  <th className="px-3 py-2">Workflow</th>
                  <th className="px-3 py-2">Provider</th>
                  <th className="px-3 py-2">Model</th>
                  <th className="px-3 py-2">Tokens</th>
                  <th className="px-3 py-2">Cost</th>
                  <th className="px-3 py-2">Latency</th>
                  <th className="px-3 py-2">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredRuns.map((run) => (
                  <tr key={run.id}>
                    <td className="max-w-xs px-3 py-3">
                      <p className="font-medium text-slate-900">
                        {run.workflow_name}
                      </p>
                      <p className="truncate text-xs text-slate-500">
                        {run.prompt_preview}
                      </p>
                    </td>
                    <td className="px-3 py-3">
                      <Badge tone={run.provider === "openai" ? "violet" : "sky"}>
                        {providerLabel(run.provider)}
                      </Badge>
                    </td>
                    <td className="px-3 py-3">{run.model}</td>
                    <td className="px-3 py-3 font-mono">
                      {run.total_tokens.toLocaleString("en-IN")}
                    </td>
                    <td className="px-3 py-3">{formatInr(run.cost_inr)}</td>
                    <td className="px-3 py-3">{run.latency_ms} ms</td>
                    <td className="px-3 py-3">
                      <Badge tone={statusTone(run.status)}>{run.status}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </SectionCard>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-1 font-mono font-semibold text-slate-950">{value}</p>
    </div>
  );
}

function providerLabel(provider: string): string {
  return provider === "openai" ? "OpenAI" : "Gemini";
}

function statusTone(status: string): "slate" | "emerald" | "amber" | "rose" {
  if (status === "succeeded" || status === "success") {
    return "emerald";
  }
  if (status === "failed") {
    return "rose";
  }
  if (status === "pending" || status === "running") {
    return "amber";
  }
  return "slate";
}
