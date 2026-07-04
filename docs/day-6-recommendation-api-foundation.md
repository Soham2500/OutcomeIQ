# OutcomeIQ — Day 6 Recommendation API Foundation

## Why Recommendations Matter

OutcomeIQ already connects AI workflow telemetry, calculated cost and verified business outcomes. The recommendation layer converts that evidence into a small set of reviewable actions. It helps a product, engineering or FinOps user identify incomplete measurement, wasted spend and optimization opportunities without requiring them to interpret every individual run.

Recommendations are suggestions only. They never change a workflow, configuration, provider or model.

## What Rule-Based Means

The MVP uses deterministic thresholds over stored workflow-run, cost and outcome data. Given the same evidence, it produces the same recommendation. It does not use machine learning, an LLM or an external API.

Before regeneration, the service removes existing `open` recommendations for the same project/workflow scope. Accepted, dismissed and resolved history is preserved.

## Recommendation Types

| Type | Trigger |
|---|---|
| `missing_costs` | One or more workflow runs have no calculated cost |
| `missing_outcomes` | One or more workflow runs have no verified outcome |
| `high_failure_rate` | At least three runs exist and final failed outcomes are at least 40% of recorded outcomes |
| `high_cost_low_success` | Spend is greater than zero, at least two runs exist and no successful outcome is recorded |
| `cost_per_success_opportunity` | At least one successful outcome allows outcome-aware unit economics |
| `data_quality` | No workflow runs are available for analysis |

## Severity and Status

Severity communicates attention level:

- `low`: informational or continuous-optimization opportunity
- `medium`: incomplete evidence affecting trustworthy economics
- `high`: material failure or spend pattern requiring investigation

Status supports a human review lifecycle:

- `open`: generated and awaiting review
- `accepted`: user agrees with the suggestion
- `dismissed`: user has chosen not to act on it
- `resolved`: the underlying issue has been addressed

Accepting or dismissing records the corresponding timestamp when one is not supplied. No status transition applies an action automatically.

## Endpoints

All endpoints require an active authenticated project member.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/recommendations/generate` | Regenerate deterministic recommendations for a project or workflow |
| GET | `/api/v1/recommendations` | List recommendations with workflow, status and type filters |
| GET | `/api/v1/recommendations/{recommendation_id}` | Read one visible recommendation |
| PATCH | `/api/v1/recommendations/{recommendation_id}` | Update its review status and optional timestamps |

## Smoke Test

With migrations applied, demo pricing seeded and the backend running:

```powershell
.\scripts\smoke_recommendation_api.ps1
```

The script creates two fully costed simulated support runs, records one successful and one failed outcome, generates and lists recommendations, then dismisses one item. Success ends with:

```text
RECOMMENDATION API SMOKE CHECK PASSED
```

## Full Verification

Run the opt-in acceptance workflow from the project root:

```powershell
.\scripts\day6_recommendation_full_verify.ps1
```

It verifies secret-file protection, installs declared dependencies, checks database readiness, runs repository checks and tests, applies reviewed migrations, verifies tables, seeds demo pricing, starts the backend only when needed and runs the recommendation smoke test.

## Intentionally Deferred

- ML-based or predictive optimization
- Autonomous routing and automated decisions
- Automatic provider or model switching
- Frontend recommendation UI
- Real provider API calls, pricing sync or billing ingestion
- Causal inference and production-grade savings attribution

The next milestone is a frontend dashboard foundation that consumes the stable dashboard and recommendation APIs.
