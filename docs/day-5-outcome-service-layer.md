# OutcomeIQ — Day 5 Outcome Service Layer

## Purpose

The outcome service layer connects workflow execution records and calculated run costs to explicit business results. It remains API-independent so authorization and transport concerns can be added separately.

## Outcome Repositories

### Outcome Contract repository

The contract repository creates, retrieves, lists and updates project-scoped definitions of success. Contract names are unique within a project. Repository functions commit and refresh changed records but intentionally contain no authorization rules.

### Workflow-run outcome repository

The run-outcome repository stores one current outcome per workflow run. Recording the same `workflow_run_id` updates its existing outcome instead of creating a duplicate. It also supports status/contract-filtered listing.

## Outcome Service

The service provides four operations:

- Create a contract after checking project existence, project-scoped name uniqueness and optional workflow ownership.
- Record or update a run outcome after validating the run and optional contract relationship.
- Retrieve a run’s current outcome.
- Calculate cost per successful outcome for optional project, workflow and configuration filters.

If a non-pending outcome does not provide `verified_at`, the service sets the current UTC timestamp. A pending outcome remains unverified unless a timestamp is explicitly supplied.

## Cost per Successful Outcome

For all workflow runs matching the selected filters:

```text
cost_per_successful_outcome_usd = total_cost_usd / successful_runs
```

- `total_cost_usd` sums available `workflow_run_costs` summaries.
- `successful_runs` counts outcomes with status `succeeded`.
- `failed_runs` counts `failed`, `escalated`, `reopened`, `abandoned` and `reversed`.
- `pending_runs` counts runs with no outcome or status `pending`.
- `success_rate` is `successful_runs / total_runs`.
- Cost per success is `null` when there are no successful runs.

Runs without a cost summary still count toward run and outcome totals. Their missing economic evidence is reported in `notes`, preventing an incomplete cost sum from appearing fully attributable.

## Status Meanings

| Status | Meaning |
|---|---|
| `succeeded` | Verified business success under the selected contract. |
| `failed` | The required business result was not achieved. |
| `escalated` | Human or higher-tier intervention was required. |
| `reopened` | A previously resolved case returned. |
| `abandoned` | The process ended without verified resolution. |
| `reversed` | Later evidence invalidated a previously accepted outcome. |
| `pending` | Evidence is incomplete or the success window remains open. |

## Intentionally Not Implemented

- Outcome HTTP APIs or smoke tests
- Endpoint authorization and membership checks
- Automated evidence ingestion or scheduled verification
- Recommendation engine
- Frontend dashboards
- Advanced causal or predictive analytics
- Aggregate metric tables

