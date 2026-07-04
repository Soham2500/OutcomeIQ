# OutcomeIQ

OutcomeIQ is an outcome-aware AI FinOps platform that connects the complete cost of AI workflows to verified business outcomes. Its initial customer-support MVP is designed to prove that the cheapest workflow per attempt may not be the cheapest workflow per successful outcome.

**GitHub:** [Soham2500/OutcomeIQ](https://github.com/Soham2500/OutcomeIQ)

## Current Development Status

- **Day 1 planning:** Complete
- **Day 2 backend foundation and closure:** 100% complete
- **FastAPI application:** Running successfully
- **Swagger UI:** Working
- **Automated tests:** 57 foundation, workflow, cost, outcome, dashboard and recommendation tests passing
- **Smoke API check:** Root, health and readiness passing
- **Day 3 database foundation:** 100% complete
- **PostgreSQL:** Local `outcomeiq_dev` connection verified
- **Database migrations/tables:** `0002_core_identity_projects` applied; all core tables exist
- **Data access layer:** Core Pydantic schemas and SQLAlchemy repositories added
- **Development seed:** Verified one safe demo row per core table
- **Authentication:** Basic register, login, bearer JWT and current-user foundation implemented
- **Organization/project APIs:** Membership-scoped reads and owner/admin updates implemented
- **Day 4 milestone:** 100% complete; auth/project smoke test passing
- **Day 5 workflow logging foundation:** Models, migration and protected simulated logging APIs implemented
- **Day 5 cost foundation:** Pricing, deterministic run-cost calculation, APIs and automation implemented
- **Day 5 outcome layer:** Storage, services, protected APIs and synthetic smoke workflow implemented
- **Day 5 milestone:** 100% complete; full verification automation available
- **Day 6 dashboard APIs:** Project overview, runs, cost and outcome summaries implemented
- **Day 6 recommendation APIs:** Deterministic, human-reviewed recommendation foundation implemented
- **Frontend:** Not implemented yet

The project currently provides a clean FastAPI modular-monolith foundation with environment-backed settings, structured logging, versioned routing, health/readiness endpoints, tests and Docker packaging.

## Technology stack

| Area | Technology |
|---|---|
| Backend | FastAPI, Python |
| Validation/settings | Pydantic, pydantic-settings |
| Planned persistence | PostgreSQL, SQLAlchemy, Alembic |
| Planned cache/jobs | Redis |
| Analytics | Pandas, Scikit-learn |
| Frontend | React, Tailwind CSS, Recharts |
| Packaging | Docker, Docker Compose |
| Testing | Pytest, HTTPX/FastAPI TestClient |

## Repository structure

```text
pro/
├── backend/                    FastAPI modular-monolith backend
│   ├── app/                    Application source
│   ├── alembic/                Migration environment and reviewed revisions
│   ├── tests/                  Backend tests
│   ├── scripts/                Future administrative scripts
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── docs/                       Product and engineering documentation
├── scripts/                    PowerShell development and verification helpers
├── .gitignore
└── README.md
```

## Completed planning documents

The Day 1 planning package contains:

- [Product understanding](docs/product-understanding.md)
- [Three-month MVP scope](docs/mvp-scope.md)
- [System architecture](docs/system-architecture.md)
- [Database design](docs/database-design.md)
- [REST API design](docs/api-design.md)
- [GitHub setup guide](docs/github-setup.md)
- [Day 2 checkpoint](docs/day-2-checkpoint.md)

These documents define the architecture and product rules that implementation must follow.

## Day 2 documentation

- [Backend foundation progress](docs/day-2-backend-foundation.md)
- [Day 2 checkpoint](docs/day-2-checkpoint.md)
- [Day 2 final summary](docs/day-2-final-summary.md)
- [GitHub setup guide](docs/github-setup.md)
- [Day 3 database setup plan](docs/day-3-database-setup-plan.md)
- [Day 3 local environment setup](docs/day-3-local-env-setup.md)
- [Safe Day 3 `.env` template](docs/day-3-env-template.md)
- [Local PostgreSQL setup](docs/postgresql-local-setup.md)
- [Day 3 checkpoint](docs/day-3-checkpoint.md)
- [First Alembic infrastructure migration](docs/day-3-alembic-migration.md)
- [Core identity and project models](docs/day-3-core-database-models.md)
- [Core data access layer](docs/day-3-core-data-access-layer.md)
- [Day 3 final summary](docs/day-3-final-summary.md)
- [Day 4 authentication readiness](docs/day-4-auth-readiness.md)
- [Day 4 starter prompt](docs/day-4-start-prompt.md)
- [Day 4 authentication testing](docs/day-4-auth-testing.md)
- [Day 4 checkpoint](docs/day-4-checkpoint.md)
- [Organization and project API guide](docs/day-4-organization-project-apis.md)
- [Manual API testing sequence](docs/day-4-manual-api-testing.md)
- [Day 4 final summary](docs/day-4-final-summary.md)
- [Day 5 workflow logging plan](docs/day-5-workflow-logging-plan.md)
- [Day 5 starter prompt](docs/day-5-start-prompt.md)
- [Day 5 workflow database models](docs/day-5-workflow-database-models.md)
- [Day 5 checkpoint](docs/day-5-checkpoint.md)
- [Day 5 workflow logging APIs](docs/day-5-workflow-logging-apis.md)
- [Day 5 cost calculation foundation](docs/day-5-cost-calculation-foundation.md)
- [Day 5 outcome models and migration](docs/day-5-outcome-models-migration.md)
- [Day 5 outcome service layer](docs/day-5-outcome-service-layer.md)
- [Day 5 outcome APIs](docs/day-5-outcome-apis.md)
- [Day 5 final summary](docs/day-5-final-summary.md)
- [Day 6 dashboard preparation](docs/day-6-dashboard-preparation.md)
- [Day 6 starter prompt](docs/day-6-start-prompt.md)
- [Day 6 dashboard analytics API](docs/day-6-dashboard-analytics-api.md)
- [Day 6 recommendation API foundation](docs/day-6-recommendation-api-foundation.md)
- [Accelerated MVP timeline](docs/accelerated-mvp-timeline.md)

## Backend foundation status

The Day 2 foundation includes:

- FastAPI application metadata and lifecycle logging
- `/api/v1` router
- Configurable CORS origins
- Environment-based application settings
- Structured JSON console logging
- Conditional SQLAlchemy engine/session foundation with no import-time connection
- Safe database `SELECT 1` readiness helper
- Alembic metadata registered with infrastructure and core identity/project models
- Applied infrastructure and core identity/project migrations
- Core Pydantic schemas, repositories and explicit development seed tooling
- Root, health and readiness routes
- Three endpoint tests plus model, authorization and diagnostic coverage
- Backend-only Docker configuration

See [Day 2 backend progress](docs/day-2-backend-foundation.md) and the [backend README](backend/README.md) for details.

## Development scripts

From the project root, PowerShell helpers are available for common tasks:

```powershell
.\scripts\check_backend.ps1
.\scripts\test_backend.ps1
.\scripts\day2_verify.ps1
.\scripts\run_backend.ps1
.\scripts\smoke_api.ps1
.\scripts\smoke_auth_project_api.ps1
.\scripts\smoke_workflow_logging_api.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\smoke_cost_calculation_api.ps1
.\scripts\smoke_outcome_tracking_api.ps1
.\scripts\day5_full_verify.ps1
.\scripts\smoke_dashboard_api.ps1
.\scripts\day6_dashboard_full_verify.ps1
.\scripts\smoke_recommendation_api.ps1
.\scripts\day6_recommendation_full_verify.ps1
.\scripts\day5_cost_full_verify.ps1
.\scripts\check_docker.ps1
.\scripts\check_db_ready.ps1
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
```

The check and verification scripts do not install packages, create databases or start Uvicorn. `run_backend.ps1` starts the server only when explicitly invoked. The smoke script expects an already-running API.

## Run the backend locally

Open Windows PowerShell and run:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Swagger UI will be available at:

```text
http://127.0.0.1:8000/docs
```

Stop the server with `Ctrl+C`.

## Run tests

From the `backend` directory with the root virtual environment activated:

```powershell
python -m pytest -v
```

Expected result:

```text
57 passed
```

The existing Starlette/HTTPX compatibility warning may remain visible; pytest is not configured to hide real warnings.

## Run the full Day 2 verification

From the project root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\day2_verify.ps1
```

The script checks required documentation, backend files, root files and the virtual environment, then runs the backend tests. A successful run ends with:

```text
DAY 2 CHECK PASSED
```

## Smoke API check

Start the API in one PowerShell window:

```powershell
.\scripts\run_backend.ps1
```

From a second PowerShell window at the project root, run:

```powershell
.\scripts\smoke_api.ps1
```

The script calls `/`, `/api/v1/health` and `/api/v1/ready`. It never starts the server automatically.

## Docker availability check

Check for the Docker CLI and Docker Compose plugin without building or starting anything:

```powershell
.\scripts\check_docker.ps1
```

## Repository formatting files

- `.gitattributes` normalizes source, documentation and PowerShell scripts to LF for consistent cross-platform Git behavior.
- `.editorconfig` standardizes UTF-8, final newlines, trailing whitespace and indentation.

After introducing `.gitattributes`, future Git operations may report normalized line-ending changes once. Review the diff before committing.

## Available endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Basic service discovery |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Current dependency readiness |
| POST | `/api/v1/auth/register` | Register a user with a securely hashed password |
| POST | `/api/v1/auth/login` | Return a bearer JWT for valid credentials |
| GET | `/api/v1/auth/me` | Return the current authenticated user |
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
| POST | `/api/v1/costs/workflow-runs/{workflow_run_id}/calculate` | Calculate and store run cost |
| GET | `/api/v1/costs/workflow-runs/{workflow_run_id}` | Read stored run cost |
| GET/POST | `/api/v1/costs/pricing-rates` | List or create configured pricing rates |
| POST/GET | `/api/v1/outcomes/contracts` | Create or list Outcome Contracts |
| GET/PATCH | `/api/v1/outcomes/contracts/{contract_id}` | Read or update an Outcome Contract |
| POST/GET | `/api/v1/outcomes/workflow-runs/{workflow_run_id}` | Record or read a run outcome |
| GET | `/api/v1/outcomes/metrics/cost-per-success` | Calculate outcome-aware unit economics |
| GET | `/api/v1/dashboard/projects/{project_id}/overview` | Project dashboard overview |
| GET | `/api/v1/dashboard/projects/{project_id}/workflow-runs` | Recent dashboard run table |
| GET | `/api/v1/dashboard/projects/{project_id}/cost-summary` | Project cost summary |
| GET | `/api/v1/dashboard/projects/{project_id}/outcome-summary` | Project outcome summary |
| POST | `/api/v1/recommendations/generate` | Generate deterministic project/workflow recommendations |
| GET | `/api/v1/recommendations` | List recommendations using project, workflow, status or type filters |
| GET | `/api/v1/recommendations/{recommendation_id}` | Read one project-visible recommendation |
| PATCH | `/api/v1/recommendations/{recommendation_id}` | Update its human-review status |
| GET | `/docs` | Swagger UI |

The readiness endpoint reports PostgreSQL as `not_configured`, `connected` or `error`. Redis remains `not_configured`. A missing database never prevents FastAPI startup.

## Day 3 database foundation complete

Create the local environment file manually if needed:

```powershell
Copy-Item backend\.env.example backend\.env
```

Edit only the private `backend\.env` file and use this format:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `YOUR_PASSWORD` locally and never commit the file. Before PostgreSQL or `.env` setup, the expected diagnostic output is `DATABASE NOT CONFIGURED`.

Check database readiness without starting FastAPI:

```powershell
.\scripts\check_db_ready.ps1
```

After PostgreSQL, `outcomeiq_dev` and the private URL are configured, the expected output is `DATABASE CONNECTED`. `DATABASE ERROR` means the configured connection could not be verified; the script does not expose the URL.

Alembic and table checks are available through project-root helper scripts:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
```

`db_migrate.ps1` is the only command above that changes database schema. It applies reviewed pending revisions through Alembic. The other scripts inspect connectivity, revision state or table existence.

Revisions `0003_workflow_logging`, `0004_cost_calculation`, `0005_outcome_tracking` and `0006_recommendations` are reviewed migration steps and are never applied by application startup. After explicit migration, the table checker reports `ALL REQUIRED TABLES EXIST`.

## Test authentication in Swagger

Start the backend, open `http://127.0.0.1:8000/docs`, register a synthetic user, log in, copy the returned access token, select **Authorize**, paste the token into the HTTP Bearer field, and call `GET /api/v1/auth/me`.

Never use real credentials in development or commit `backend/.env`. See [Day 4 authentication testing](docs/day-4-auth-testing.md) for the complete walkthrough.

## Next development steps

### Day 6 recommendation API foundation

- Day 4 authentication, organization and project API foundation is complete
- `AUTH PROJECT API SMOKE CHECK PASSED` is the verified live result
- Models prepared: `workflows`, `workflow_configurations`, `workflow_runs`, `model_calls`, `tool_calls`
- Protected workflow logging APIs and a synthetic end-to-end smoke script are implemented
- Apply the reviewed revision explicitly with `.\scripts\db_migrate.ps1`
- Verify all tables with `.\scripts\check_db_tables.ps1`
- Day 5 records simulated telemetry only; no real provider keys or production data
- Run the live workflow check with `.\scripts\smoke_workflow_logging_api.ps1`
- Demo pricing, deterministic Decimal cost calculation and protected cost APIs are implemented
- Run the full cost verification with `.\scripts\day5_cost_full_verify.ps1`
- OutcomeIQ’s core cost-per-success proof is represented end to end in the backend
- Run the complete acceptance path with `.\scripts\day5_full_verify.ps1`
- Day 6 dashboard analytics API foundation is implemented
- Run its complete acceptance path with `.\scripts\day6_dashboard_full_verify.ps1`
- Deterministic recommendation storage, rules and protected APIs are implemented
- Run its complete acceptance path with `.\scripts\day6_recommendation_full_verify.ps1`
- Next milestone: frontend dashboard foundation
- Real provider calls, billing sync, autonomous decisions and frontend remain deferred

Continue with the [Day 6 recommendation foundation](docs/day-6-recommendation-api-foundation.md). Never commit `backend/.env`, store provider secrets, or persist raw prompts/responses.
