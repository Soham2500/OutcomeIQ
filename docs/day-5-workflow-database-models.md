# OutcomeIQ — Day 5 Workflow Database Models

## Purpose

Workflow logging is the evidence layer beneath OutcomeIQ. Before the platform can calculate cost per successful outcome, it must reliably reconstruct each workflow execution: the selected configuration, every model and tool call, token usage, latency, retries, fallbacks and estimated direct cost. This milestone records those facts without attempting outcome verification or business recommendations.

## Tables

### `workflows`

Defines a stable AI workflow within a project, such as **AI Support Ticket Resolution**. A project-scoped unique slug prevents ambiguous workflow identity. Lifecycle status supports active, inactive and archived workflows.

### `workflow_configurations`

Defines a named, versioned execution strategy for a workflow. Examples include `quality-first v1`, `economy-first v1` and `balanced v2`. `config_json` may contain non-secret synthetic configuration details; it must not contain provider credentials.

### `workflow_runs`

Represents one execution attempt. It links the project, workflow and optional configuration while recording trigger type, status, safe summaries, timestamps, latency and an optional external reference such as a synthetic support-ticket ID.

### `model_calls`

Records each model invocation in execution order. It captures provider/model identity, call type, status, prompt/completion/total token counts, latency, nullable estimated USD cost and explicit retry/fallback flags.

### `tool_calls`

Records each internal or external tool invocation in execution order. It captures the tool name, status, latency, nullable estimated USD cost, safe summaries and errors.

## Relationship Flow

```text
project
  └── workflow
        ├── workflow configuration
        └── workflow run
              ├── model calls
              └── tool calls
```

A run may omit its configuration only for compatibility with manually captured telemetry. Every model call and tool call belongs to exactly one workflow run.

## Safe Data to Store

- Synthetic or redacted workflow and configuration names
- Provider/model/tool identifiers
- Statuses, trigger types and sequence numbers
- Token counts, latency and timestamps
- Nullable estimated cost values with explicit currency naming
- Synthetic external references
- Short redacted summaries and non-secret metadata

## Data That Must Not Be Stored

- API keys, passwords, bearer tokens or connection strings
- Raw prompts or full model responses
- Unredacted customer messages, personal data or production payloads
- Tool credentials or sensitive request/response bodies
- Secrets embedded in `config_json` or `metadata_json`

## Retry and Fallback Tracking

`model_calls.is_retry` marks a repeated attempt and `model_calls.is_fallback` marks use of an alternate path. Together with status, sequence, tokens, latency and estimated cost, these fields provide the future evidence needed to measure retry/fallback waste. No waste calculation is implemented in this milestone.

## Migration and Verification

The migration is prepared but is not applied automatically. From the project root, review migration history and then explicitly apply it:

```powershell
.\scripts\db_history.ps1
.\scripts\db_migrate.ps1
```

Verify all core and workflow tables:

```powershell
.\scripts\check_db_tables.ps1
```

After migration, the expected result is:

```text
ALL REQUIRED TABLES EXIST
```

Before migration, the checker intentionally lists the five missing workflow tables.

## Intentionally Not Implemented

- Workflow logging repositories or HTTP APIs
- Real AI-provider or tool calls
- Outcome Contracts and outcome verification
- Cost attribution, failure-waste analytics or configuration comparison
- Recommendation engine or autonomous routing
- Frontend and dashboards
- Outcome, cost-summary, analytics or recommendation tables

