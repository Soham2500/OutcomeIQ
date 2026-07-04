# OutcomeIQ — Day 5 Workflow Logging Plan

## Day 5 Objective

Build the first durable workflow-telemetry foundation inside the existing project boundary. Day 5 should model and record an AI workflow, one execution run, its model calls and its tool calls without yet calculating verified outcomes, recommendations or advanced analytics.

## Why Workflow Logging Is Core to OutcomeIQ

OutcomeIQ cannot calculate cost per successful business outcome unless it first reconstructs the complete economic path of every run. Workflow logging supplies the authoritative evidence: which configuration executed, which model/tool calls occurred, how long they took, which calls retried or fell back, how many tokens were consumed and what raw cost inputs were observed.

The logging layer must remain factual. It records evidence; it does not yet decide whether the workflow succeeded or whether a configuration should scale or stop.

## Planned Tables

### `workflows`

Defines a monitored AI workflow within one project. It should hold stable identity, a project foreign key, name/slug, lifecycle status and timestamps.

### `workflow_runs`

Represents one execution attempt of a workflow/configuration. It should capture identifiers, lifecycle status, start/end timing, total latency and safe correlation/idempotency context.

### `model_calls`

Records each model invocation belonging to a workflow run: provider/model identifiers, sequence, token usage, latency, retry/fallback markers, status and raw cost fields. Prompts, responses, API keys and sensitive customer content must not be stored.

### `tool_calls`

Records each external tool invocation belonging to a workflow run: tool identity, sequence, latency, status, retry marker and raw cost fields. Tool credentials and sensitive payloads must not be stored.

## Planned Concepts

- **Configuration:** The executable model/tool choices associated with a run. Day 5 may use a minimal safe representation while preserving a path to immutable configurations later.
- **Workflow run:** One traceable execution unit within a project-owned workflow.
- **Model call:** One LLM/model operation within the run.
- **Tool call:** One external tool operation within the run.
- **Retry/fallback marker:** Explicit evidence that a call repeated or used an alternate provider/model/tool path.
- **Latency:** Time measured per call and per run using consistent units.
- **Token usage:** Input and output token counts stored as non-negative integers.
- **Raw cost fields:** Direct provider/tool cost observations or raw pricing inputs, clearly distinguished from later attributed/derived economics.

## Day 5 Deliverables

1. Review `docs/database-design.md` and preserve the FastAPI modular-monolith architecture.
2. Define the four SQLAlchemy models and their foreign keys/indexes.
3. Register only the approved models with `Base.metadata`.
4. Create one reviewed Alembic revision chained from the current head.
5. Add repositories and Pydantic schemas without HTTP APIs unless explicitly approved.
6. Add safe table-inspection/verification scripts.
7. Add tests that validate imports, metadata and schema contracts without real provider calls.

## What Not to Build on Day 5

- Frontend or dashboards
- Advanced analytics or comparisons
- Recommendation engine
- Outcome Contracts or outcome verification
- Cost attribution/failure-waste calculations
- Autonomous model routing
- Real OpenAI/Anthropic/cloud provider calls
- Large multi-agent orchestration

## Safety Rules

- Never store or print real API keys, bearer tokens or provider credentials.
- Simulated model/tool calls are allowed and preferred.
- Never persist raw prompts, model responses, customer messages or production data.
- Store only redacted/synthetic references and numeric usage evidence.
- Do not place secrets in JSON metadata or logs.
- Do not auto-run migrations or create tables at application startup.
- Use synthetic local data and reviewed, reversible migrations only.

## Completion Signal

Day 5 is complete when the reviewed migration creates exactly the four approved workflow logging tables, foreign-key relationships are valid, safe verification reports that they exist, tests pass, and simulated logging evidence can be represented without any real provider integration.
