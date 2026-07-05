# OutcomeIQ — Day 7 Dashboard Charts and Demo Data

## Purpose

This increment makes OutcomeIQ locally demonstrable. The dashboard now explains workflow economics visually, while an explicit API seed creates a repeatable customer-support dataset through the same authenticated endpoints used by the product.

## Chart Components

The frontend uses Recharts for two compact evidence views:

- `CostByRunChart` — bar chart of calculated cost for recent workflow runs
- `OutcomeStatusChart` — successful, failed and pending outcome distribution

Two Tailwind-based explanatory components complement the charts:

- `SuccessRateCard` — percentage and progress indicator with a definition
- `CostOutcomeInsight` — total cost, successful outcomes and cost per successful outcome beneath the core message: “Cheapest request is not always cheapest successful outcome.”

All components tolerate empty arrays, missing identifiers and nullable/string decimal values.

## Dashboard Sections

The project dashboard now contains:

1. Project selector and explicit refresh action
2. Total-run, total-cost, success-rate and cost-per-success summary cards
3. Recent-run cost and outcome-distribution charts
4. OutcomeIQ cost/outcome insight
5. Recent workflow-run evidence table
6. Loading, API-error, no-project and no-run states

The backend remains authoritative for every business metric.

## Demo Data Flow

Start the backend and seed the explicitly non-production pricing rates:

```powershell
.\scripts\db_migrate.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\run_backend.ps1
```

From another project-root PowerShell window:

```powershell
.\scripts\seed_demo_data_via_api.ps1
```

The seed reuses the fixed demo organization/project/workflow/configuration when they already exist, then creates five fresh simulated runs: three successful, one failed and one escalated. Each run includes model calls, a tool call, calculated cost and a verified outcome. Recommendations are generated after the evidence is recorded.

A successful run ends with:

```text
DEMO DATA SEED PASSED
```

## Full Verification

With PostgreSQL available and the backend already running:

```powershell
.\scripts\day7_dashboard_charts_verify.ps1
```

The verifier checks private environment-file protection, installs frontend dependencies, runs TypeScript validation, checks database readiness, applies reviewed migrations, seeds demo pricing, verifies backend health and runs the API demo seed. It does not start either server.

## Run the Frontend

```powershell
.\scripts\install_frontend.ps1
.\scripts\run_frontend.ps1
```

Open `http://127.0.0.1:5173`.

Demo login:

```text
Email: demo@outcomeiq.local
Password: Demo@12345
```

These are local synthetic demo credentials, not production secrets.

## Login Troubleshooting

### `OPTIONS /api/v1/auth/login` returns 400

The browser CORS preflight is being rejected. Restart the backend after updating the code. OutcomeIQ explicitly allows both Vite origins:

```text
http://localhost:5173
http://127.0.0.1:5173
```

It also allows the equivalent local port `3000` origins. The runtime settings always include these approved development origins even when an older private `backend/.env` contains a shorter CORS list.

### `POST /api/v1/auth/login` returns 401

The credentials are not valid for a current local user. With the backend running, seed the demo account and evidence:

```powershell
.\scripts\seed_demo_data_via_api.ps1
```

Alternatively, register a new user from the frontend. The seed now tries login first, registers only when needed, and uses a unique local demo email if the fixed address already belongs to an account with a different password. It prints the active demo email without exposing a token.

## Intentionally Not Implemented

- Production authentication/session polish
- Advanced interactive or predictive charts
- Real cloud/provider billing synchronization
- Real AI-provider calls or API keys
- Autonomous routing or automatic model switching
- Production deployment

The next milestone is a polished, reproducible end-to-end demonstration with configuration comparison and concise presentation evidence.
