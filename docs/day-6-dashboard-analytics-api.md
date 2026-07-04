# OutcomeIQ — Day 6 Dashboard Analytics API

## Why Dashboard Analytics APIs Are Needed

OutcomeIQ’s raw workflow, cost and outcome APIs provide detailed evidence, but a dashboard client should not reconstruct business metrics from dozens of records. The Day 6 analytics layer exposes stable, read-only project summaries while preserving one source of truth for cost per successful outcome.

All dashboard endpoints require an active authenticated project member. No aggregate tables were introduced; summaries are calculated from current workflow, cost and outcome records.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/dashboard/projects/{project_id}/overview` | Project-level workflow, run, cost and outcome overview |
| GET | `/api/v1/dashboard/projects/{project_id}/workflow-runs` | Recent run table with workflow, cost and outcome context |
| GET | `/api/v1/dashboard/projects/{project_id}/cost-summary` | Aggregated tokens, calls and model/tool/total cost |
| GET | `/api/v1/dashboard/projects/{project_id}/outcome-summary` | Outcome counts, success rate and cost per success |

## Project Overview

The overview combines:

- Workflow and workflow-run counts
- Technical run status counts
- Total calculated cost
- Successful and failed business outcomes
- Outcome success rate
- Cost per successful outcome
- Notes about incomplete cost evidence

Technical run completion and business success remain separate. A technically succeeded run can still have a failed, escalated, reopened, abandoned or reversed business outcome.

## Workflow Runs Table

The run endpoint returns recent runs newest first with pagination. Each row includes workflow identity/name, configuration, technical status, timestamps, calculated cost when available, business outcome status and a nullable success flag.

Project ownership for run listing and every related dashboard summary follows the canonical relationship:

```text
WorkflowRun.workflow_id -> Workflow.id -> Workflow.project_id
```

The analytics layer does not rely on `configuration_id`, organization identity or an Outcome Contract to decide whether a run belongs to a project.

The nullable success flag is:

- `true` for a verified `succeeded` outcome
- `false` for final unsuccessful outcome statuses
- `null` when the outcome is missing or pending

## Cost Summary

The cost summary adds all available run-cost records for the project:

- Model, tool and total USD cost
- Total tokens
- Model/tool call counts
- Average cost across runs with calculated cost
- Highest-cost workflow run

Runs without a calculated cost are not included in monetary averages. The project overview’s evidence notes report missing cost summaries through the existing outcome metrics service.

## Outcome Summary

The outcome summary reuses the established cost-per-success service. It returns total, successful, failed and pending runs, plus success rate and cost per successful outcome. Reusing the service prevents dashboard and outcome endpoints from drifting into different formulas.

## Smoke Test

Apply migrations and seed the explicitly non-production demo rates, then start the backend:

```powershell
.\scripts\db_migrate.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\run_backend.ps1
```

From another project-root PowerShell window:

```powershell
.\scripts\smoke_dashboard_api.ps1
```

The script creates two synthetic costed runs with one success and one failure. A successful run ends with:

```text
DASHBOARD API SMOKE CHECK PASSED
```

## Full Verification

Run the opt-in end-to-end Day 6 verifier:

```powershell
.\scripts\day6_dashboard_full_verify.ps1
```

It checks secret-file protection, dependencies, database readiness, tests, migrations, tables and demo pricing before running the dashboard smoke test. It stops only a backend process that it started.

## Intentionally Not Implemented

- Frontend dashboard
- Automated decisions or autonomous workflow changes
- Forecasting, anomaly detection or predictive analytics
- New analytics aggregate tables
- Real AI-provider billing/pricing synchronization
- Production deployment

## Recommendation Foundation Added

The next backend slice is now available: deterministic, evidence-backed recommendation APIs can flag missing costs, missing outcomes, high failure patterns, spend without success and cost-per-success opportunities. Recommendations remain human-reviewed suggestions and never alter workflow configurations. See [Day 6 recommendation API foundation](day-6-recommendation-api-foundation.md).

The next product milestone is the frontend dashboard foundation consuming these stable analytics and recommendation endpoints.
