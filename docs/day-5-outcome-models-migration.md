# OutcomeIQ — Day 5 Outcome Models and Migration

## Why Outcome Tracking Matters

Token and workflow cost alone cannot answer OutcomeIQ’s central question: **what did the workflow cost per successful business outcome?** Outcome tracking adds the business evidence required to distinguish a technically completed run from a genuinely successful result.

This milestone defines storage only. It does not verify outcomes, calculate cost per success, or make recommendations.

## `outcome_contracts`

An Outcome Contract defines what success means before a workflow run is evaluated. It belongs to a project and may be scoped to one workflow. The contract stores a human-readable name and description, structured success criteria, a verification window, lifecycle status and authorship.

Example contract:

> Ticket resolved without escalation and not reopened within 48 hours.

The `success_criteria_json` field must contain structured, non-secret criteria only. API keys, customer messages, credentials and production personal data must never be stored there.

## `workflow_run_outcomes`

A workflow run has at most one current outcome record. The record optionally links to the contract used for evaluation and stores outcome status, verification source, optional score/business value, verification time, notes and safe metadata.

The workflow execution status and business outcome status are deliberately separate. A run can execute successfully while its business outcome later becomes `failed`, `reopened` or `reversed`.

## Outcome Status Meanings

| Status | Meaning |
|---|---|
| `pending` | Verification evidence is incomplete or the success window is still open. |
| `succeeded` | The contract’s success criteria were verified. |
| `failed` | The required business result was not achieved. |
| `escalated` | Human or higher-tier intervention was required. |
| `reopened` | A previously resolved case returned within the relevant window. |
| `abandoned` | The process ended without a verified resolution. |
| `reversed` | A previously accepted outcome was invalidated by later evidence. |

Verification sources are `manual`, `simulated`, `api` and `system`. These values describe evidence origin; they do not imply confidence or correctness by themselves.

## Migration

Revision `0005_outcome_tracking` creates exactly:

- `outcome_contracts`
- `workflow_run_outcomes`

Review migration history and apply pending revisions explicitly from the project root:

```powershell
.\scripts\db_history.ps1
.\scripts\db_migrate.ps1
```

Verify required tables:

```powershell
.\scripts\check_db_tables.ps1
```

After migration, the expected result is:

```text
ALL REQUIRED TABLES EXIST
```

## Intentionally Not Implemented

- Outcome schemas, repositories, services or HTTP APIs
- Automated or manual verification workflows
- Outcome evidence ingestion
- Cost per successful outcome
- Failure-waste analysis
- Recommendation engine or autonomous routing
- Frontend dashboards
- Real AI-provider integrations

