# OutcomeIQ — Day 5 Cost Calculation Foundation

## Why Cost Calculation Matters

Workflow telemetry becomes useful FinOps evidence only when tokens and tool usage can be translated into reproducible monetary estimates. OutcomeIQ now calculates the direct estimated cost of a recorded workflow run while preserving where each number came from. This is a cost foundation, not yet cost-per-outcome analytics.

## Database Tables

### `model_pricing_rates`

Stores explicit input/output token prices per 1,000 tokens for a provider/model/currency and optional effective window. Rates are locally configured; no provider API or billing account is queried. Effective dates allow later calculations to select an applicable version without overwriting historical pricing definitions.

### `workflow_run_costs`

Stores one recalculable summary per workflow run: token totals, model/tool call counts, model cost, tool cost, total cost, calculation status, evidence notes and calculation timestamp. Re-running the calculation updates the same summary instead of creating duplicates.

## Formula

For each model call with an active USD rate:

```text
model call cost =
  (prompt_tokens / 1000 × input_token_price_per_1k)
  +
  (completion_tokens / 1000 × output_token_price_per_1k)
```

The run calculation then applies:

```text
model_cost_usd = sum(model call costs)
tool_cost_usd  = sum(recorded tool estimated_cost_usd values)
total_cost_usd = model_cost_usd + tool_cost_usd
```

All monetary arithmetic uses `Decimal` and is rounded to eight decimal places. If a model rate is absent, the recorded model-call estimate is used when available. Missing or fallback evidence marks the summary `partial` and adds a calculation note; it is not silently represented as fully known cost.

## Demo Pricing Warning

The seed contains synthetic demonstration rates for:

- `simulated / support-classifier-small`
- `simulated / support-generator-standard`
- `openai / gpt-demo-placeholder`

These values are examples only. They are not current or authoritative provider prices and must not be used for production billing decisions.

Seed them after applying the migration:

```powershell
.\scripts\db_seed_pricing.ps1
```

## Cost API Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/costs/workflow-runs/{workflow_run_id}/calculate` | Calculate and upsert an authorized run summary |
| GET | `/api/v1/costs/workflow-runs/{workflow_run_id}` | Read an existing authorized run summary |
| GET | `/api/v1/costs/pricing-rates` | List configured pricing rates |
| POST | `/api/v1/costs/pricing-rates` | Create a pricing rate; authenticated MVP access |

Run-cost endpoints enforce project membership. Pricing-rate endpoints require an active authenticated user; advanced administrative authorization is deferred.

## Manual Verification

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\run_backend.ps1
```

From a second project-root PowerShell window:

```powershell
.\scripts\smoke_cost_calculation_api.ps1
```

The smoke test uses only synthetic workflows, simulated model identities and redacted summaries. Success ends with `COST CALCULATION API SMOKE CHECK PASSED`.

## Full Automation

Run the opt-in full workflow from the project root:

```powershell
.\scripts\day5_cost_full_verify.ps1
```

It verifies that `backend/.env` is Git-ignored, installs declared dependencies, checks connectivity, runs repository verification and pytest, applies reviewed migrations, checks tables, seeds demo pricing, reuses or temporarily starts the backend, and runs the cost smoke test. A backend process started by the script is stopped in `finally`; an already-running backend is left untouched.

The script does not display secrets, modify `backend/.env`, commit files or push to GitHub.

## Intentionally Not Implemented

- Outcome tracking or verified cost per successful outcome
- Failure-waste analysis and recommendation engine
- Frontend dashboards
- Real provider billing or pricing synchronization
- Autonomous routing or model switching
- Production rate approval/governance workflow

