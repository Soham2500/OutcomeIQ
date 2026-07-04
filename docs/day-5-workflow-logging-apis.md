# OutcomeIQ — Day 5 Workflow Logging APIs

## Purpose

The first workflow logging API records a complete simulated execution trace inside an authorized project. It creates workflows and versioned configurations, starts runs, records model/tool telemetry, transitions runs to succeeded or failed, and reconstructs a sequence-ordered trace.

This layer stores evidence only. Raw estimated cost may be supplied by a trusted caller, but OutcomeIQ does not calculate, attribute or interpret cost yet.

## Prerequisite

The reviewed Day 5 migration must be applied before using these endpoints:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

The table check should report `ALL REQUIRED TABLES EXIST`.

## Endpoints

All endpoints require a valid bearer token.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/workflows` | Create a project workflow; owner/admin required |
| GET | `/api/v1/workflows` | List member-visible workflows, optionally by project |
| GET | `/api/v1/workflows/{workflow_id}` | Read a member-visible workflow |
| PATCH | `/api/v1/workflows/{workflow_id}` | Update a workflow; owner/admin required |
| POST | `/api/v1/workflows/{workflow_id}/configurations` | Create a versioned configuration; owner/admin required |
| GET | `/api/v1/workflows/{workflow_id}/configurations` | List configurations for project members |
| POST | `/api/v1/workflow-runs` | Start a run with status `running` |
| GET | `/api/v1/workflow-runs` | List member-visible runs with optional filters |
| GET | `/api/v1/workflow-runs/{workflow_run_id}` | Read one member-visible run |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/model-calls` | Record redacted model telemetry |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/tool-calls` | Record redacted tool telemetry |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/complete` | Transition a running run to `succeeded` |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/fail` | Transition a running run to `failed` |
| GET | `/api/v1/workflow-runs/{workflow_run_id}/trace` | Return run, ordered model calls and ordered tool calls |

## Logging Flow

```text
create workflow
  -> create configuration
  -> start run
  -> record model calls
  -> record tool calls
  -> complete or fail run
  -> retrieve trace
```

The workflow and optional configuration must belong to the run’s project/workflow. Telemetry can only be added while the run is `running`.

## Sample Request Bodies

Create a workflow:

```json
{
  "project_id": "00000000-0000-0000-0000-000000000001",
  "name": "AI Support Ticket Resolution",
  "slug": "ai-support-ticket-resolution",
  "description": "Synthetic support workflow"
}
```

Create a configuration:

```json
{
  "name": "Balanced configuration",
  "version_label": "balanced-v1",
  "strategy_name": "balanced",
  "config_json": {
    "provider_mode": "simulated"
  }
}
```

Start a run:

```json
{
  "project_id": "00000000-0000-0000-0000-000000000001",
  "workflow_id": "00000000-0000-0000-0000-000000000002",
  "configuration_id": "00000000-0000-0000-0000-000000000003",
  "trigger_type": "simulated",
  "external_reference": "support-ticket-123",
  "input_summary": "Synthetic payment issue ticket"
}
```

Record a model call:

```json
{
  "sequence_number": 1,
  "provider": "simulated",
  "model_name": "simulated-classifier-v1",
  "call_type": "classification",
  "status": "succeeded",
  "prompt_tokens": 120,
  "completion_tokens": 12,
  "total_tokens": 132,
  "latency_ms": 180,
  "request_summary": "Redacted synthetic classification input",
  "response_summary": "Payment issue category"
}
```

Record a tool call:

```json
{
  "sequence_number": 2,
  "tool_name": "ticket_status_check",
  "status": "succeeded",
  "latency_ms": 90,
  "input_summary": "Synthetic ticket reference",
  "output_summary": "Payment marked for review"
}
```

Complete a run:

```json
{
  "output_summary": "Synthetic support response completed",
  "latency_ms": 690,
  "metadata_json": {
    "execution_mode": "simulated"
  }
}
```

## Smoke Test

Start the backend in one PowerShell window. In a second window at the project root, run:

```powershell
.\scripts\smoke_workflow_logging_api.ps1
```

The script registers a unique local user and creates synthetic organization, project, workflow, configuration and trace data. It uses simulated provider/model names, never prints the password or token, and ends with:

```text
WORKFLOW LOGGING API SMOKE CHECK PASSED
```

## Data Safety

Store only redacted summaries and synthetic metadata. Never send API keys, credentials, bearer tokens, raw prompts, full model responses, production customer content or personal data in summaries or JSON metadata.

## Intentionally Not Implemented

- Real AI-provider or tool integrations
- Provider pricing lookup or cost calculation engine
- Complete workflow-cost attribution and failure-waste analysis
- Outcome Contracts or outcome verification
- Configuration recommendations or autonomous routing
- Frontend and dashboards

