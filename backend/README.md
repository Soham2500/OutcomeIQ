# OutcomeIQ Backend

Initial FastAPI modular-monolith foundation for the OutcomeIQ outcome-aware AI FinOps platform.

## Current status

**Day 2 through Day 5 are complete, the Day 6 dashboard/recommendation APIs are implemented, and a separate Day 7 React frontend now consumes them.** The backend remains the source of truth for analytics and recommendation rules.

Available now:

- FastAPI application setup
- Versioned API router
- Root, health and readiness endpoints
- Environment-backed settings
- Configurable CORS origins
- Structured JSON logging
- SQLAlchemy declarative base with approved infrastructure and core models
- Conditional engine and session factory when `DATABASE_URL` is present
- Safe database readiness check using `SELECT 1`
- Alembic environment with approved core, workflow and cost models registered
- First infrastructure migration for `system_metadata`
- Applied core migration for users, organizations, projects, memberships and audit events
- Pydantic schemas and SQLAlchemy repositories for core records
- Explicit, idempotent local development seed tooling
- Read-only schema inspection and Alembic-state validation
- Bcrypt password hashing and JWT access-token utilities
- Register, login and protected current-user endpoints
- Authenticated organization/project CRUD endpoints with audit events
- Automatic owner membership for newly created projects
- Membership-scoped project listing/read access and owner/admin updates
- Safe shared audit service and live auth/project API smoke test
- Workflow, workflow-configuration, run, model-call and tool-call models
- Explicit workflow and cost Alembic revisions
- Workflow schemas, repositories and run-state validation service
- Protected workflow/configuration/run/call/trace endpoints
- Synthetic workflow logging API smoke script
- Model pricing-rate and workflow-run-cost models
- Decimal-based cost calculation with partial-evidence notes
- Protected cost and pricing-rate APIs
- Idempotent demo pricing seed and full Day 5 verification automation
- Outcome Contract and one-per-run outcome models with `0005_outcome_tracking`
- Outcome schemas, repositories, verification timestamping and cost-per-success service
- Membership-scoped Outcome Contract, run-outcome and unit-economics APIs
- Two-run synthetic outcome tracking smoke test
- Full Day 5 readiness, migration, seed and smoke-test automation
- Read-only dashboard schemas, analytics service and four protected project endpoints
- Synthetic dashboard smoke test and full Day 6 verification automation
- Recommendation model and `0006_recommendations` migration
- Deterministic missing-evidence, failure and cost-per-success recommendation rules
- Protected generate, list, read and status-update recommendation endpoints
- Synthetic recommendation smoke test and full verification automation
- Separate React/TypeScript frontend with typed clients for auth, projects, dashboard analytics and recommendations
- Recharts cost/outcome visuals and repeatable API-based five-run demo data flow
- Endpoint, model and access-layer tests
- Docker packaging
- Root Compose stack with PostgreSQL, FastAPI and nginx/React services
- Deterministic three-workflow/twelve-run demo fixture and live-quality gates
- Placeholder production environment contract and non-deploying pre-deploy gate
- Render/Vercel manual deployment runbook and public production smoke check
- Final go-live, rollback, troubleshooting and launch-note documentation
- Day 14 launch-safety endpoints for readiness and admin billing inspection
- Config-based admin billing access with masked provider IDs and hidden raw payment payloads

Not implemented yet:

- Advanced authentication such as refresh tokens, reset, MFA or SSO
- Automated outcome evidence ingestion and scheduled verification
- ML-based recommendation optimization or autonomous actions
- Advanced cost-per-outcome cohorts and failure-waste analytics
- Real provider pricing or billing synchronization
- Live payment capture
- Redis integration
- Actual production deployment and complete UX polish

## Prerequisites

- Python 3.11 or newer; Python 3.12 is recommended
- `pip`
- Docker Desktop only if using Docker

## Developer scripts

The repository provides PowerShell helpers. Run them from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_backend.ps1
.\scripts\test_backend.ps1
.\scripts\day2_verify.ps1
.\scripts\run_backend.ps1
.\scripts\smoke_api.ps1
.\scripts\smoke_workflow_logging_api.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\smoke_cost_calculation_api.ps1
.\scripts\smoke_outcome_tracking_api.ps1
.\scripts\day5_full_verify.ps1
.\scripts\smoke_dashboard_api.ps1
.\scripts\day6_dashboard_full_verify.ps1
.\scripts\smoke_recommendation_api.ps1
.\scripts\day6_recommendation_full_verify.ps1
.\scripts\install_frontend.ps1
.\scripts\run_frontend.ps1
.\scripts\frontend_typecheck.ps1
.\scripts\day7_frontend_foundation_verify.ps1
.\scripts\seed_demo_data_via_api.ps1
.\scripts\day7_dashboard_charts_verify.ps1
.\scripts\docker_build.ps1
.\scripts\docker_up.ps1
.\scripts\docker_migrate.ps1
.\scripts\docker_seed_pricing.ps1
.\scripts\docker_logs.ps1
.\scripts\docker_backend_shell.ps1
.\scripts\docker_verify.ps1
.\scripts\docker_down.ps1
.\scripts\db_seed_demo.ps1
.\scripts\docker_seed_demo.ps1
.\scripts\live_quality_gate.ps1
.\scripts\live_docker_quality_gate.ps1
.\scripts\pre_deploy_check.ps1
.\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
.\scripts\day14_launch_safety_verify.ps1
.\scripts\day5_cost_full_verify.ps1
.\scripts\check_docker.ps1
.\scripts\check_db_ready.ps1
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

- `check_backend.ps1` verifies the expected structure without changing anything.
- `test_backend.ps1` activates `.venv` and runs pytest.
- `day2_verify.ps1` checks all Day 1/2 deliverables and runs tests.
- `run_backend.ps1` activates `.venv` and starts Uvicorn with auto-reload.
- `smoke_api.ps1` checks the three running API endpoints from another terminal.
- `smoke_workflow_logging_api.ps1` records one complete synthetic workflow trace against an already-running API.
- `db_seed_pricing.ps1` idempotently inserts explicitly non-production demo rates.
- `smoke_cost_calculation_api.ps1` calculates and reads one synthetic run cost.
- `smoke_outcome_tracking_api.ps1` verifies one success, one escalation and cost per success.
- `day5_full_verify.ps1` runs the complete opt-in Day 5 acceptance sequence and cleans up only its own backend process.
- `smoke_dashboard_api.ps1` verifies overview, run, cost and outcome summaries with synthetic data.
- `day6_dashboard_full_verify.ps1` performs the complete opt-in dashboard acceptance sequence.
- `smoke_recommendation_api.ps1` generates, lists and dismisses an evidence-backed recommendation using simulated data.
- `day6_recommendation_full_verify.ps1` performs the complete opt-in recommendation acceptance sequence.
- `install_frontend.ps1` installs the declared React/Vite dependencies.
- `run_frontend.ps1` explicitly starts the Vite development server.
- `frontend_typecheck.ps1` validates the TypeScript project without starting it.
- `day7_frontend_foundation_verify.ps1` checks secret protection, installs dependencies and runs the frontend typecheck.
- `seed_demo_data_via_api.ps1` creates five simulated, fully costed and outcome-verified support runs through authenticated APIs.
- `day7_dashboard_charts_verify.ps1` validates the frontend, database readiness and opt-in local demo flow without starting servers.
- `docker_verify.ps1` builds and verifies the complete local PostgreSQL/backend/frontend stack.
- `docker_down.ps1` stops containers without deleting the named database volume.
- `db_seed_demo.ps1` converges the local database on the deterministic support dataset.
- `live_quality_gate.ps1` runs the complete host tests, build, database, seed and smoke sequence.
- `live_docker_quality_gate.ps1` verifies the container stack and deterministic Docker seed.
- `pre_deploy_check.ps1` validates secret safety, tests, frontend build and the host live-quality gate without deploying.
- `prod_smoke_check.ps1` checks public backend health/docs and the frontend homepage after a manual deployment; it does not log in or expose secrets.
- `day14_launch_safety_verify.ps1` checks launch-safety files and runs the frontend production build.
- `day5_cost_full_verify.ps1` performs the opt-in migration, seed, startup and cost smoke workflow safely.
- `check_docker.ps1` reports Docker and Compose availability without starting anything.
- `check_db_ready.ps1` reports database configuration/connectivity without creating databases, tables or migrations.
- `db_seed_dev.ps1` explicitly inserts only the safe demo identity/project records.
- `check_core_data.ps1` reports core row counts and demo-data presence without changing data.
- `inspect_db_schema.ps1` lists safe table and column metadata without changing data.
- `validate_alembic_state.ps1` confirms migration files and the current database head without running migrations.
- `db_history.ps1` and `db_current.ps1` inspect Alembic state.
- `db_migrate.ps1` explicitly applies reviewed migrations through `alembic upgrade head`.
- `check_db_tables.ps1` safely checks all required core, workflow and cost tables.

Deployment preparation documents:

- `docs/render-deployment-guide.md` — manual Render backend/database and Render/Vercel frontend sequence
- `docs/deployment-checklist.md` — before, during and after-deployment acceptance checklist
- `docs/one-month-live-cost-plan.md` — bounded one-month public MVP cost plan
- `docs/deployment-runbook.md` — final operator sequence from local checks through browser validation
- `docs/final-go-live-checklist.md` — evidence-based go/no-go decision checklist
- `docs/rollback-checklist.md` — manual containment, rollback and secret-rotation steps
- `docs/production-troubleshooting.md` — production symptom and recovery guide
- `docs/launch-notes-template.md` — sanitized v0.1 release record template

The first live version must use only the simulated AI provider. Add real AI APIs later only after token limits, monthly budget caps, model allowlists, complete call logging and a provider kill switch are implemented.

Day 14 launch-safety documents:

- `docs/day-14-launch-safety-summary.md`
- `docs/production-payment-go-live-checklist.md`
- `docs/legal-policy-pages-guide.md`
- `docs/admin-billing-view-guide.md`

## Setup on Windows PowerShell

Open PowerShell and begin at the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
```

Create the root virtual environment:

```powershell
python -m venv .venv
```

Allow activation scripts for the current PowerShell process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

Move into the backend directory:

```powershell
cd backend
```

Create a local environment file if one does not already exist:

```powershell
Copy-Item .env.example .env
```

No PostgreSQL or Redis URL is required for FastAPI startup. An empty `DATABASE_URL` reports `not_configured`.

## Run the FastAPI server

From the `backend` directory with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Readiness: `http://127.0.0.1:8000/api/v1/ready`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Available endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Basic service discovery |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Dependency readiness; database is `not_configured`, `connected` or `error` |
| POST | `/api/v1/auth/register` | Compatibility alias that sends registration email OTP; does not activate immediately |
| POST | `/api/v1/auth/register/request-otp` | Send or resend registration email OTP for a pending account |
| POST | `/api/v1/auth/register/verify-otp` | Verify OTP and create the active user |
| POST | `/api/v1/auth/login` | Return a bearer access token |
| GET | `/api/v1/auth/me` | Return the authenticated active user |
| POST/GET | `/api/v1/organizations` | Create or list organizations |
| GET/PATCH | `/api/v1/organizations/{organization_id}` | Read or update an organization |
| POST/GET | `/api/v1/projects` | Create or list projects |
| GET/PATCH | `/api/v1/projects/{project_id}` | Read or update a project |
| GET | `/api/v1/projects/{project_id}/members` | List project memberships |
| POST/GET | `/api/v1/workflows` | Create or list authorized workflows |
| GET/PATCH | `/api/v1/workflows/{workflow_id}` | Read or update a workflow |
| POST/GET | `/api/v1/workflows/{workflow_id}/configurations` | Create or list configurations |
| POST/GET | `/api/v1/workflow-runs` | Start or list workflow runs |
| GET | `/api/v1/workflow-runs/{workflow_run_id}` | Read a workflow run |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/model-calls` | Record simulated model telemetry |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/tool-calls` | Record simulated tool telemetry |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/complete` | Complete a running workflow run |
| POST | `/api/v1/workflow-runs/{workflow_run_id}/fail` | Fail a running workflow run |
| GET | `/api/v1/workflow-runs/{workflow_run_id}/trace` | Read the ordered run trace |
| POST | `/api/v1/costs/workflow-runs/{workflow_run_id}/calculate` | Calculate and upsert run cost |
| GET | `/api/v1/costs/workflow-runs/{workflow_run_id}` | Read stored run cost |
| GET/POST | `/api/v1/costs/pricing-rates` | List or create configured pricing rates |
| POST/GET | `/api/v1/outcomes/contracts` | Create or list Outcome Contracts |
| GET/PATCH | `/api/v1/outcomes/contracts/{contract_id}` | Read or update a contract |
| POST/GET | `/api/v1/outcomes/workflow-runs/{workflow_run_id}` | Record or read a run outcome |
| GET | `/api/v1/outcomes/metrics/cost-per-success` | Calculate cost per successful outcome |
| GET | `/api/v1/dashboard/projects/{project_id}/overview` | Project dashboard overview |
| GET | `/api/v1/dashboard/projects/{project_id}/workflow-runs` | Recent workflow-run summary table |
| GET | `/api/v1/dashboard/projects/{project_id}/cost-summary` | Project cost summary |
| GET | `/api/v1/dashboard/projects/{project_id}/outcome-summary` | Project outcome summary |
| POST | `/api/v1/recommendations/generate` | Generate deterministic project/workflow recommendations |
| GET | `/api/v1/recommendations` | List project recommendations with optional filters |
| GET | `/api/v1/recommendations/{recommendation_id}` | Read one visible recommendation |
| PATCH | `/api/v1/recommendations/{recommendation_id}` | Update its human-review status |
| GET | `/docs` | Swagger UI |

## Stop the server

Press `Ctrl+C` in the PowerShell window running Uvicorn.

## Run the smoke API check

Keep Uvicorn running in the first PowerShell window. Open a second PowerShell window and run from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\smoke_api.ps1
```

The smoke script reports a helpful failure if the API is not running; it never launches Uvicorn itself.

## Run tests

From the `backend` directory:

```powershell
python -m pytest -v
```

Expected result:

```text
58 passed
```

Run only the health tests when needed:

```powershell
python -m pytest tests\test_health.py -v
```

The pytest configuration intentionally leaves warnings visible.

The current `StarletteDeprecationWarning` related to FastAPI TestClient and HTTPX is non-blocking. It does not change the `58 passed` result and should remain visible until the upstream compatibility path is addressed deliberately.

## Verified commands

From the project root:

```powershell
.\scripts\day2_verify.ps1
.\scripts\test_backend.ps1
.\scripts\run_backend.ps1
```

With the API running in the first window, use a second PowerShell window:

```powershell
.\scripts\smoke_api.ps1
```

Verified results are 58 passing tests, including local CORS preflight, auth, workflow logging, cost arithmetic, outcome unit economics, dashboard ownership joins and recommendation rules/routes.

## Run with Docker

Docker Desktop must be installed and running.

From the project root, build and verify the complete three-service stack:

```powershell
.\scripts\docker_verify.ps1
```

Open:

- Backend: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:8080`

Stop containers while preserving PostgreSQL data:

```powershell
.\scripts\docker_down.ps1
```

The root Compose credentials are local demo placeholders only. The older `backend/docker-compose.yml` remains a backend-only development helper; use the root Compose stack for the full application.

## Configuration

Settings load from environment variables or `backend\.env`. Available values are documented in `.env.example`.

Current optional placeholders:

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`

Do not use the example JWT secret in a deployed environment.

## Database foundation

Create `backend\.env` manually from the safe example if needed:

```powershell
Copy-Item .env.example .env
```

Set the private local value using this format:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `YOUR_PASSWORD` locally. Never commit or print the completed URL.

From the project root, check status with:

```powershell
.\scripts\check_db_ready.ps1
```

The result is one of:

- `DATABASE NOT CONFIGURED` before `.env`/URL setup; acceptable in early Day 3
- `DATABASE CONNECTED` after PostgreSQL and credentials are correct
- `DATABASE ERROR` when configured connectivity fails or the script cannot complete

The check performs only `SELECT 1`. It never creates a database, table or migration.

## First Alembic infrastructure migration

Alembic uses the private `DATABASE_URL` from application settings and `Base.metadata` from `app/db/base.py`. Metadata now contains `SystemMetadata` plus the approved user, organization, project, project-membership and audit-event models.

From the project root, inspect migration state with:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
```

Apply any pending reviewed migration explicitly, then verify the table:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

Revisions `0003_workflow_logging`, `0004_cost_calculation` and `0005_outcome_tracking` are explicit reviewed steps and are never run by application startup. The table checker lists any pending workflow, cost or outcome tables; after explicit migration it reports `ALL REQUIRED TABLES EXIST`.

## Development seed and core data check

The seed is never run at application startup. Invoke it explicitly from the project root:

```powershell
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
```

The verified local seed contains one user, organization, project, project membership and audit event. The checker reports `CORE DEVELOPMENT DATA FOUND`.

## Day 3 database foundation complete

Run the final read-only database checks from the project root:

```powershell
.\scripts\check_db_ready.ps1
.\scripts\check_db_tables.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
```

Expected key results are `DATABASE CONNECTED`, `ALL CORE TABLES EXIST`, `CORE DEVELOPMENT DATA FOUND` and `ALEMBIC STATE VALID`.

## Day 4 authentication foundation

Install the declared authentication dependencies from the project root:

```powershell
pip install -r backend\requirements.txt
```

Run the backend, open `http://127.0.0.1:8000/docs`, register a synthetic user, log in, copy the returned access token, select Swagger's **Authorize** button, and call `/api/v1/auth/me`.

After authorization, create an organization, create a project with the returned organization ID, list projects and inspect `/api/v1/projects/{project_id}/members`. The project creator should have role `owner`. See `docs/day-4-manual-api-testing.md` for the complete sequence.

With the backend already running and PostgreSQL connected, run the live local smoke path from another PowerShell window:

```powershell
.\scripts\smoke_auth_project_api.ps1
```

This creates timestamped synthetic local data. It does not start the server, run migrations, delete rows or print the password/access token.

`backend/.env` must remain ignored. Never hardcode or print `JWT_SECRET_KEY`, and never expose `hashed_password` through an API schema or response.

## Troubleshooting

### PowerShell blocks virtual-environment activation

Run this in the same PowerShell window, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run these commands from the project root. If already inside `backend`, return to the root first with `cd ..`.

### `python` is not recognized

Try the Windows Python launcher:

```powershell
py -m venv .venv
```

If neither `python` nor `py` works, reinstall Python and select **Add Python to PATH**.

### `ModuleNotFoundError: app`

Confirm Uvicorn and pytest are running from:

```text
C:\Users\soham\OneDrive\Documents\pro\backend
```

Also confirm the root virtual environment is active.

### `ModuleNotFoundError: fastapi`

Activate the virtual environment and reinstall dependencies from the project root:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Port 8000 is already in use

Use a different port:

```powershell
uvicorn app.main:app --reload --port 8001
```

### Swagger UI does not open

Confirm Uvicorn shows a successful startup and open `http://127.0.0.1:8000/docs`, not the filesystem path.

### Docker cannot start

Confirm Docker Desktop is running and configured for Linux containers.

## Day 5 complete

The live Day 4 smoke result is `AUTH PROJECT API SMOKE CHECK PASSED`. Day 5 now defines `workflows`, `workflow_configurations`, `workflow_runs`, `model_calls` and `tool_calls` without applying the migration automatically.

After reviewing the migration, apply and verify it from the project root:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

After the migration is applied, start the backend and run the synthetic end-to-end trace from another project-root PowerShell window:

```powershell
.\scripts\smoke_workflow_logging_api.ps1
```

Seed the demo rates and run the cost smoke test manually, or use the complete opt-in verifier:

```powershell
.\scripts\db_seed_pricing.ps1
.\scripts\smoke_cost_calculation_api.ps1
.\scripts\day5_cost_full_verify.ps1
```

OutcomeIQ’s core cost-per-success proof is represented in the backend. Run the complete acceptance sequence with:

```powershell
.\scripts\day5_full_verify.ps1
```

The backend, frontend and PostgreSQL now run together through the root production-like local Compose stack. Run `.\scripts\docker_verify.ps1` for container verification, then follow `docs/deployment-runbook.md` for manual hosting and final validation. The first live version remains simulated and needs no real AI-provider key. Actual cloud deployment, real provider integrations and autonomous actions remain deferred until explicitly performed.
