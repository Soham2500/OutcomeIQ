import { getApiErrorMessage, isApiStatus } from "./client";
import {
  calculateWorkflowRunCost,
  createPricingRate,
  listPricingRates,
} from "./costsApi";
import {
  createOutcomeContract,
  listOutcomeContracts,
  recordWorkflowRunOutcome,
} from "./outcomesApi";
import {
  completeWorkflowRun,
  failWorkflowRun,
  recordModelCall,
  recordToolCall,
  startWorkflowRun,
} from "./workflowRunsApi";
import {
  createWorkflow,
  createWorkflowConfiguration,
  listWorkflowConfigurations,
  listWorkflows,
} from "./workflowsApi";
import type { DemoScenarioSummary } from "../types/demo";
import type { Workflow, WorkflowConfiguration } from "../types/workflow";

const WORKFLOW_NAME = "Support Ticket Classifier";
const CONTRACT_NAME = "Ticket Resolution Success";

const demoRates = [
  {
    provider: "simulated",
    model_name: "support-classifier-small",
    input_token_price_per_1k: 0.0002,
    output_token_price_per_1k: 0.0004,
  },
  {
    provider: "simulated",
    model_name: "support-generator-standard",
    input_token_price_per_1k: 0.001,
    output_token_price_per_1k: 0.002,
  },
];

function createSlug(value: string): string {
  const base = value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);
  return `${base || "outcomeiq"}-${Date.now().toString().slice(-8)}`;
}

async function ensureDemoPricingRates() {
  const existingRates = await listPricingRates("simulated");
  const existingModels = new Set(existingRates.map((rate) => rate.model_name));

  await Promise.all(
    demoRates
      .filter((rate) => !existingModels.has(rate.model_name))
      .map(async (rate) => {
        try {
          await createPricingRate({
            ...rate,
            currency: "INR",
            is_active: true,
            metadata_json: {
              source: "frontend_demo_scenario",
              note: "Simulated MVP pricing only",
            },
          });
        } catch (error) {
          if (!isApiStatus(error, 400)) {
            throw error;
          }
        }
      }),
  );
}

async function getOrCreateWorkflow(projectId: string): Promise<Workflow> {
  const workflows = await listWorkflows(projectId);
  const existing = workflows.find((workflow) => workflow.name === WORKFLOW_NAME);
  if (existing) {
    return existing;
  }
  return createWorkflow({
    project_id: projectId,
    name: WORKFLOW_NAME,
    slug: createSlug(WORKFLOW_NAME),
    description:
      "Simulated AI customer-support workflow for outcome-aware FinOps demo.",
  });
}

async function getOrCreateConfiguration(
  workflowId: string,
): Promise<WorkflowConfiguration> {
  const configurations = await listWorkflowConfigurations(workflowId);
  const existing = configurations.find(
    (configuration) => configuration.version_label === "demo-v1",
  );
  if (existing) {
    return existing;
  }
  return createWorkflowConfiguration(workflowId, {
    name: "Simulated support workflow configuration",
    version_label: "demo-v1",
    description: "Frontend demo configuration using simulated provider data.",
    strategy_name: "balanced",
    config_json: {
      provider_mode: "simulated",
      no_real_ai_api_calls: true,
    },
  });
}

async function getOrCreateOutcomeContract(projectId: string, workflowId: string) {
  const contracts = await listOutcomeContracts({
    project_id: projectId,
    workflow_id: workflowId,
  });
  const existing = contracts.find((contract) => contract.name === CONTRACT_NAME);
  if (existing) {
    return existing;
  }
  return createOutcomeContract({
    project_id: projectId,
    workflow_id: workflowId,
    name: CONTRACT_NAME,
    description:
      "Ticket is resolved without customer escalation and without reopening inside the evidence window.",
    success_criteria_json: {
      resolved: true,
      escalated: false,
      not_reopened_within_hours: 48,
    },
    success_window_hours: 48,
  });
}

async function createSuccessfulRun(
  projectId: string,
  workflowId: string,
  configurationId: string,
) {
  const run = await startWorkflowRun({
    project_id: projectId,
    workflow_id: workflowId,
    configuration_id: configurationId,
    trigger_type: "simulated",
    external_reference: `frontend-demo-success-${Date.now()}`,
    input_summary: 'Customer ticket: "My payment failed but money was deducted."',
    metadata_json: { demo_case: "payment_failed_money_deducted" },
  });

  await recordModelCall(run.id, {
    sequence_number: 1,
    provider: "simulated",
    model_name: "support-classifier-small",
    call_type: "classification",
    status: "succeeded",
    prompt_tokens: 950,
    completion_tokens: 180,
    total_tokens: 1130,
    latency_ms: 180,
    request_summary: "Classify payment failure ticket",
    response_summary: "Billing/payment failure category",
  });
  await recordModelCall(run.id, {
    sequence_number: 2,
    provider: "simulated",
    model_name: "support-generator-standard",
    call_type: "generation",
    status: "succeeded",
    prompt_tokens: 1200,
    completion_tokens: 450,
    total_tokens: 1650,
    latency_ms: 420,
    request_summary: "Generate customer-safe support response",
    response_summary: "Refund verification and reassurance response",
  });
  await recordToolCall(run.id, {
    sequence_number: 3,
    tool_name: "ticket_lookup",
    status: "succeeded",
    latency_ms: 90,
    estimated_cost_usd: 0.0005,
    input_summary: "Synthetic ticket reference",
    output_summary: "Payment captured; refund workflow available",
  });
  await completeWorkflowRun(run.id, {
    output_summary: "Customer ticket resolved with clear refund guidance.",
    latency_ms: 690,
  });
  await calculateWorkflowRunCost(run.id);
  return run;
}

async function createFailedRun(
  projectId: string,
  workflowId: string,
  configurationId: string,
) {
  const run = await startWorkflowRun({
    project_id: projectId,
    workflow_id: workflowId,
    configuration_id: configurationId,
    trigger_type: "simulated",
    external_reference: `frontend-demo-failure-${Date.now()}`,
    input_summary: 'Customer ticket: "My payment failed but money was deducted."',
    metadata_json: { demo_case: "payment_failed_money_deducted_retry" },
  });

  await recordModelCall(run.id, {
    sequence_number: 1,
    provider: "simulated",
    model_name: "support-classifier-small",
    call_type: "classification",
    status: "succeeded",
    prompt_tokens: 950,
    completion_tokens: 180,
    total_tokens: 1130,
    latency_ms: 200,
    request_summary: "Classify payment failure ticket",
    response_summary: "Billing/payment failure category",
  });
  await recordModelCall(run.id, {
    sequence_number: 2,
    provider: "simulated",
    model_name: "support-generator-standard",
    call_type: "generation",
    status: "failed",
    prompt_tokens: 1250,
    completion_tokens: 120,
    total_tokens: 1370,
    latency_ms: 520,
    request_summary: "Generate customer-safe support response",
    response_summary: "Incomplete response generated",
    error_message: "Simulated confidence below support threshold.",
  });
  await recordModelCall(run.id, {
    sequence_number: 3,
    provider: "simulated",
    model_name: "support-generator-standard",
    call_type: "fallback_generation",
    status: "succeeded",
    prompt_tokens: 1600,
    completion_tokens: 380,
    total_tokens: 1980,
    latency_ms: 640,
    is_fallback: true,
    request_summary: "Fallback generation after low confidence",
    response_summary: "Escalation response generated",
  });
  await recordToolCall(run.id, {
    sequence_number: 4,
    tool_name: "ticket_lookup",
    status: "succeeded",
    latency_ms: 110,
    estimated_cost_usd: 0.0005,
    input_summary: "Synthetic ticket reference",
    output_summary: "Payment state ambiguous; manual review required",
  });
  await failWorkflowRun(run.id, {
    error_message: "Simulated workflow escalated because outcome confidence was low.",
    latency_ms: 1470,
  });
  await calculateWorkflowRunCost(run.id);
  return run;
}

export async function runDemoScenario(
  projectId: string,
): Promise<DemoScenarioSummary> {
  if (!projectId) {
    throw new Error("Select a project before running demo data.");
  }

  try {
    await ensureDemoPricingRates();
    const workflow = await getOrCreateWorkflow(projectId);
    const configuration = await getOrCreateConfiguration(workflow.id);
    const contract = await getOrCreateOutcomeContract(projectId, workflow.id);

    const runA = await createSuccessfulRun(
      projectId,
      workflow.id,
      configuration.id,
    );
    await recordWorkflowRunOutcome(runA.id, {
      outcome_contract_id: contract.id,
      status: "succeeded",
      verification_source: "simulated",
      outcome_score: 1,
      notes: "Simulated customer issue resolved without escalation.",
    });

    const runB = await createFailedRun(projectId, workflow.id, configuration.id);
    await recordWorkflowRunOutcome(runB.id, {
      outcome_contract_id: contract.id,
      status: "failed",
      verification_source: "simulated",
      outcome_score: 0,
      notes: "Simulated workflow consumed cost but failed the business outcome.",
    });

    return {
      workflow_id: workflow.id,
      run_a_id: runA.id,
      run_b_id: runB.id,
      total_runs_created: 2,
      message:
        "Simulated support workflow data created. Dashboard and recommendations can now be refreshed.",
    };
  } catch (error) {
    throw new Error(
      getApiErrorMessage(
        error,
        "Demo scenario could not be completed. Check backend, database migrations and simulated pricing setup.",
      ),
    );
  }
}
