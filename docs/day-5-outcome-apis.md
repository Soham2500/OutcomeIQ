# OutcomeIQ — Day 5 Outcome APIs

## Purpose

The protected outcome API connects registered workflows, calculated run costs and verified business results. It exposes Outcome Contract management, one current outcome per workflow run, and on-demand cost-per-success metrics without creating aggregate or recommendation tables.

All endpoints require an active bearer-authenticated user and are scoped to project memberships.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/outcomes/contracts` | Create a project Outcome Contract |
| GET | `/api/v1/outcomes/contracts` | List member-visible contracts with optional filters |
| GET | `/api/v1/outcomes/contracts/{contract_id}` | Read one member-visible contract |
| PATCH | `/api/v1/outcomes/contracts/{contract_id}` | Update a member-visible contract |
| POST | `/api/v1/outcomes/workflow-runs/{workflow_run_id}` | Create or update a run outcome |
| GET | `/api/v1/outcomes/workflow-runs/{workflow_run_id}` | Read a run’s current outcome |
| GET | `/api/v1/outcomes/metrics/cost-per-success` | Calculate outcome-aware unit economics |

## Outcome Contracts

An Outcome Contract defines success before a run is judged. A customer-support example is:

> Ticket resolved without escalation and not reopened within 48 hours.

The contract stores a project/workflow scope, structured non-secret criteria and the time window in which later evidence may reverse or reopen the result.

## Workflow-run Outcomes

Each workflow run has at most one current outcome. Posting again updates that record. Non-pending outcomes receive a UTC `verified_at` timestamp when the caller does not provide one. The service validates that an optional contract belongs to the run’s project and applies to its workflow.

## Cost per Successful Outcome

The metrics endpoint supports optional `project_id`, `workflow_id` and `configuration_id` filters. Without a project filter, it still aggregates only projects visible to the authenticated user.

```text
cost_per_successful_outcome_usd = total_cost_usd / successful_runs
```

Successful, failed and pending counts use recorded business outcomes rather than technical workflow-run completion. Runs without cost summaries remain counted and produce an evidence note.

## Smoke Test

Apply migrations and seed the explicitly non-production pricing rates first:

```powershell
.\scripts\db_migrate.ps1
.\scripts\db_seed_pricing.ps1
```

Start the backend in one PowerShell window. From a second project-root window run:

```powershell
.\scripts\smoke_outcome_tracking_api.ps1
```

The script creates two fully synthetic costed workflow runs, records one successful and one escalated outcome, validates cost-per-success metrics and ends with:

```text
OUTCOME TRACKING API SMOKE CHECK PASSED
```

It never prints the password or bearer token and never calls a real AI provider.

## Intentionally Not Implemented

- Recommendation engine or scale/stop decisions
- Frontend dashboards
- Advanced causal, predictive or cohort analytics
- Autonomous routing or model switching
- Real AI-provider or billing integrations
- Automated evidence ingestion and scheduled outcome reversal

