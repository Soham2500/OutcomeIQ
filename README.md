# OutcomeIQ

OutcomeIQ is an outcome-aware AI FinOps platform that connects the complete cost of AI workflows to verified business outcomes. Its initial customer-support MVP is designed to prove that the cheapest workflow per attempt may not be the cheapest workflow per successful outcome.

**GitHub:** [Soham2500/OutcomeIQ](https://github.com/Soham2500/OutcomeIQ)

## Current Development Status

- **Day 1 planning:** Complete
- **Day 2 backend foundation and closure:** 100% complete
- **FastAPI application:** Running successfully
- **Swagger UI:** Working
- **Automated tests:** 58 foundation, CORS, workflow, cost, outcome, dashboard and recommendation tests passing
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
- **Day 7 frontend:** React/Vite dashboard, auth, projects and recommendations foundation implemented
- **Day 7 demo:** Cost/outcome charts and repeatable five-run API demo data flow implemented
- **Day 8 frontend polish:** Presentation-ready shell and protected evaluator Demo Guide implemented
- **Day 8 Docker:** PostgreSQL, FastAPI and nginx/React local production-like stack implemented
- **Live-quality hardening:** Deterministic demo fixture plus host and Docker quality gates implemented
- **Pre-deployment readiness:** Placeholder production environment contracts and non-deploying gate implemented
- **Deployment runbook:** Render/Vercel guide, checklist, public smoke tooling and one-month cost plan implemented
- **Go-live operations:** Final manual runbook, go/no-go checklist, rollback procedure, troubleshooting guide and launch-note template implemented

OutcomeIQ is moving from fast MVP construction to live-quality MVP hardening. Fast delivery is allowed only when tests, builds, secret checks, migrations and applicable end-to-end gates remain green.

The project currently provides a clean FastAPI modular-monolith foundation with environment-backed settings, structured logging, versioned routing, health/readiness endpoints, tests and Docker packaging.

## Technology stack

| Area | Technology |
|---|---|
| Backend | FastAPI, Python |
| Validation/settings | Pydantic, pydantic-settings |
| Planned persistence | PostgreSQL, SQLAlchemy, Alembic |
| Planned cache/jobs | Redis |
| Analytics | Pandas, Scikit-learn |
| Frontend | React, TypeScript, Vite, Tailwind CSS, React Router, Axios, Recharts |
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
├── frontend/                   React/TypeScript Vite application
│   ├── src/                    Pages, components, API client and types
│   └── package.json
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
- [Day 7 frontend dashboard foundation](docs/day-7-frontend-dashboard-foundation.md)
- [Day 7 dashboard charts and demo data](docs/day-7-dashboard-charts-demo-data.md)
- [Day 8 frontend polish and demo walkthrough](docs/day-8-frontend-polish-demo-walkthrough.md)
- [Day 8 Docker local production setup](docs/day-8-docker-local-production-setup.md)
- [Deterministic demo data guide](docs/demo-data-guide.md)
- [Live-readiness checklist](docs/live-readiness-checklist.md)
- [Production environment and pre-deploy checks](docs/day-9-production-env-and-predeploy.md)
- [Render and Vercel deployment guide](docs/render-deployment-guide.md)
- [Deployment checklist](docs/deployment-checklist.md)
- [One-month live cost plan](docs/one-month-live-cost-plan.md)
- [Final manual deployment runbook](docs/deployment-runbook.md)
- [Final go-live checklist](docs/final-go-live-checklist.md)
- [Rollback checklist](docs/rollback-checklist.md)
- [Production troubleshooting guide](docs/production-troubleshooting.md)
- [Launch notes template](docs/launch-notes-template.md)
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
.\scripts\install_frontend.ps1
.\scripts\run_frontend.ps1
.\scripts\frontend_typecheck.ps1
.\scripts\day7_frontend_foundation_verify.ps1
.\scripts\seed_demo_data_via_api.ps1
.\scripts\day7_dashboard_charts_verify.ps1
.\scripts\day8_frontend_polish_verify.ps1
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

Backend check scripts do not start Uvicorn implicitly. `run_backend.ps1` and `run_frontend.ps1` start their development servers only when explicitly invoked. The Day 7 verifier installs declared frontend dependencies and runs TypeScript validation; it does not open a browser.

## Run the full stack with Docker

Start Docker Desktop, then run the production-like local verification from the project root:

```powershell
.\scripts\docker_verify.ps1
```

After it passes:

- Frontend: `http://127.0.0.1:8080`
- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`

Stop containers without deleting PostgreSQL data:

```powershell
.\scripts\docker_down.ps1
```

The credentials in `docker-compose.yml` are local demo placeholders, not production secrets. See [Docker local production setup](docs/day-8-docker-local-production-setup.md).

## Live-quality gates

Run the complete host-based quality gate:

```powershell
.\scripts\live_quality_gate.ps1
```

Run the complete container-based quality gate with Docker Desktop running:

```powershell
.\scripts\live_docker_quality_gate.ps1
```

Seed only the deterministic local demo fixture:

```powershell
.\scripts\db_seed_demo.ps1
```

The seed converges on three customer-support workflows and twelve stable runs instead of creating uncontrolled duplicates.

Run the non-deploying production-readiness check:

```powershell
.\scripts\pre_deploy_check.ps1
```

The first live version remains intentionally simulated: it uses no real AI-provider keys or billing integrations.

After manually deploying the backend and frontend, verify their public unauthenticated surfaces:

```powershell
.\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
```

Follow the [Render and Vercel deployment guide](docs/render-deployment-guide.md), complete the [deployment checklist](docs/deployment-checklist.md), and approve the [one-month cost plan](docs/one-month-live-cost-plan.md) before provisioning paid resources. The next step is manual deployment; repository scripts do not create cloud resources.

For the launch window, follow the [final deployment runbook](docs/deployment-runbook.md), make the go/no-go decision with the [final checklist](docs/final-go-live-checklist.md), and keep the [rollback checklist](docs/rollback-checklist.md) open. Use the [production troubleshooting guide](docs/production-troubleshooting.md) for failures and the [launch notes template](docs/launch-notes-template.md) to record a sanitized release.

The first live version must remain on the simulated AI provider. Real AI APIs should be considered only after token limits, monthly budget caps, model allowlists, complete model-call logging and a provider kill switch are implemented.

## Frontend Demo Flow

The Day 9 frontend polish makes the core MVP demo operable from the UI without using Swagger for the basic flow.

1. Start Docker, or start the local backend and frontend separately.
2. Register or login.
3. Create an organization and project from **Projects**.
4. Run simulated demo data from **Projects**, **Workflows**, **Dashboard**, or **Recommendations**.
5. Open **Dashboard** to view workflow runs, total cost, success rate and cost per successful outcome.
6. Open **Recommendations** and generate evidence-backed recommendations.
7. Open **Demo Guide** for the viva/demo explanation.

The UI demo uses simulated provider/model data only. It does not call real AI APIs and does not require provider keys.

Verify the Day 9 frontend polish:

```powershell
.\scripts\day9_frontend_polish_verify.ps1
```

## Day 10 Demo Flow

The Day 10 upgrade adds a stronger live-demo experience with an Analytics page, browser-only exports and more polished dashboard/recommendation explanations.

1. Start the app with local scripts or Docker.
2. Login/register.
3. Create a project.
4. Run demo data.
5. Open **Dashboard**.
6. Open **Analytics**.
7. Export JSON/CSV.
8. Generate Recommendations.
9. Open **Demo Guide**.

Verify the Day 10 upgrade:

```powershell
.\scripts\day10_major_upgrade_verify.ps1
```

The MVP uses simulated provider data. Real AI provider integration and real cloud billing integration are future scope.

## Subscription-ready billing foundation

OutcomeIQ now includes a test/sandbox billing architecture for early SaaS launch preparation:

- Free, Starter and Pro plan model
- Current subscription API
- Usage counters for projects and workflow runs
- Backend-owned soft usage limits
- Pricing page
- Billing page
- Test-mode plan activation
- Razorpay webhook storage placeholder

Real payments are not enabled yet. Razorpay live mode is a future step after KYC, privacy policy, terms, refund/cancellation policy, verified webhooks and production checks. API keys must be stored only in backend environment variables.

Seed billing plans after applying migrations:

```powershell
.\scripts\db_migrate.ps1
.\scripts\db_seed_plans.ps1
```

Verify the billing foundation:

```powershell
.\scripts\day11_billing_foundation_verify.ps1
```

### Test subscription flow

1. Register/login.
2. Create project.
3. Open **Pricing**.
4. Upgrade to Starter in test mode.
5. Open **Billing**.
6. Check usage limits.
7. Run demo data.
8. Open Dashboard.
9. Generate recommendations.

See [subscription billing architecture](docs/subscription-billing-architecture.md), [Razorpay test-mode setup](docs/razorpay-test-mode-setup.md), and [early live launch plan](docs/early-live-launch-plan.md).

## Razorpay Test Mode Billing

OutcomeIQ supports Razorpay test-mode checkout preparation for Starter and Pro plans. Real payments are not enabled.

- Backend creates test checkout payloads only when Razorpay test env vars are configured.
- Frontend receives only safe public checkout fields such as `key_id`.
- Frontend never stores Razorpay secrets.
- Backend verifies Razorpay webhook signatures when `RAZORPAY_WEBHOOK_SECRET` is configured.
- Local fallback activation remains available for demos without Razorpay keys.

Verify the Razorpay test-mode foundation:

```powershell
.\scripts\day13_razorpay_test_verify.ps1
```

Test a local webhook payload:

```powershell
.\scripts\test_razorpay_webhook.ps1
```

See [Day 13 Razorpay test mode](docs/day-13-razorpay-test-mode.md). Keep Razorpay live mode disabled until KYC, policies, webhook testing and production verification are complete.

## Payment Gateway Setup

OutcomeIQ now supports backend-controlled Razorpay subscription checkout. The browser can open Razorpay Checkout, but subscription status is controlled by the backend after webhook verification or explicit local test activation.

Use test mode first:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
RAZORPAY_CHECKOUT_ENABLED=true
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
RAZORPAY_STARTER_PLAN_ID=
RAZORPAY_PRO_PLAN_ID=
```

Rules:

- Do not commit Razorpay key CSV files.
- Do not commit `backend/.env` or `frontend/.env`.
- Do not put `RAZORPAY_KEY_SECRET` or webhook secret in frontend code.
- Only the public `RAZORPAY_KEY_ID` may be returned to the frontend when checkout is allowed.
- Live checkout works only when `PAYMENTS_LIVE_ENABLED=true` and `RAZORPAY_MODE=live`.
- If live mode is requested while live payments are disabled, backend checkout is rejected safely.

Verify the payment-gateway layer:

```powershell
.\scripts\day15_payment_gateway_verify.ps1
```

References:

- [Day 15 payment gateway](docs/day-15-payment-gateway-on.md)
- [Razorpay live-mode go-live guide](docs/razorpay-live-mode-go-live.md)

## Payment Runtime Testing

Day 15 verifies the payment gateway code and frontend build. Day 16 verifies the running billing/payment surfaces without charging real money.

Start the backend, then run:

```powershell
.\scripts\day16_payment_runtime_smoke.ps1
```

Verify Day 16 files and frontend build:

```powershell
.\scripts\day16_payment_runtime_verify.ps1
```

Runtime testing rules:

- Use Razorpay test mode first.
- Do not use live cards in test mode.
- Do not commit `.env` files, `rzp-key.csv`, Razorpay CSV exports, key files or webhook secrets.
- Checkout and Billing pages should be tested through an authenticated browser session.
- Real payments should be enabled only after Render/Vercel deployment, webhook verification, public policy pages and the go-live checklist are complete.

## AWS Deployment Quickstart

Recommended early MVP architecture:

- Frontend: AWS Amplify Hosting
- Backend: AWS Lightsail instance running Docker
- Database: PostgreSQL container on the same Lightsail instance
- Payments: Razorpay test/live-ready webhook

This keeps the first deployment simple and low-cost. Avoid ECS/Fargate, RDS, ALB and NAT Gateway until the MVP has real usage that justifies the extra cost.

Verify AWS deployment readiness:

```powershell
.\scripts\day17_aws_deployment_ready_verify.ps1
```

After manual deployment, run:

```powershell
.\scripts\aws_live_smoke_check.ps1 -BackendUrl "https://api.yourdomain.com" -FrontendUrl "https://your-amplify-domain.amplifyapp.com"
```

AWS deployment references:

- [Day 17 AWS deployment guide](docs/day-17-aws-deployment-guide.md)
- [AWS Lightsail environment variables](docs/aws-lightsail-env-vars.md)
- [AWS cost safety checklist](docs/aws-cost-safety-checklist.md)
- [AWS Amplify frontend guide](docs/aws-amplify-frontend-guide.md)
- [AWS Razorpay webhook guide](docs/aws-razorpay-webhook-guide.md)

Secret safety:

- Do not commit `backend/.env` or `frontend/.env`.
- Do not commit AWS access keys.
- Do not commit Razorpay key CSV files.
- Keep Razorpay secrets only in the backend server environment.
- Configure Razorpay webhook as `https://api.yourdomain.com/api/v1/billing/webhook/razorpay`.
- Keep `PAYMENTS_LIVE_ENABLED=false` until HTTPS, policy pages, webhook verification and rollback checks are complete.

Quick deployment commands on Lightsail:

```bash
cd /opt/outcomeiq
cp backend/.env.aws.example backend/.env
nano backend/.env
docker compose -f docker-compose.aws.yml up -d --build
docker compose -f docker-compose.aws.yml exec backend alembic upgrade head
```

See the short guide: [AWS deployment quickstart](docs/aws-deployment-quickstart.md).

## Launch Safety and Policy Pages

Day 14 adds launch-safety surfaces for public MVP review while keeping real payments and real AI calls disabled.

Public policy pages:

- `/privacy`
- `/terms`
- `/refund-policy`
- `/contact`

Operational launch-safety pages:

- `/launch-readiness`
- `/admin/billing` — hidden from the sidebar and restricted by backend `ADMIN_EMAILS`

Backend launch-safety endpoints:

- `GET /api/v1/launch/readiness`
- `GET /api/v1/admin/billing/overview`
- `GET /api/v1/admin/billing/subscriptions`
- `GET /api/v1/admin/billing/payment-events`
- `GET /api/v1/admin/billing/usage`

Safety configuration defaults:

```text
PAYMENTS_LIVE_ENABLED=false
APP_PUBLIC_URL=
SUPPORT_EMAIL=
ADMIN_EMAILS=admin@example.com
```

Real payments remain disabled unless `PAYMENTS_LIVE_ENABLED` is intentionally enabled after legal, payment-provider, webhook and operational approval. Pricing and Billing show a visible test-mode banner; Demo Guide discloses that the MVP uses simulated AI provider data.

Verify the launch-safety layer:

```powershell
.\scripts\day14_launch_safety_verify.ps1
```

Documentation:

- [Day 14 launch safety summary](docs/day-14-launch-safety-summary.md)
- [Production payment go-live checklist](docs/production-payment-go-live-checklist.md)
- [Legal policy pages guide](docs/legal-policy-pages-guide.md)
- [Admin billing view guide](docs/admin-billing-view-guide.md)

## Live Deployment

OutcomeIQ’s early live deployment target is:

- Backend: Render Web Service
- Database: Render PostgreSQL
- Frontend: Vercel
- Payments: subscription-ready test mode only

Deployment references:

- [Day 12 live deployment guide](docs/day-12-live-deployment-guide.md)
- [Render/Vercel environment variables](docs/render-vercel-env-vars.md)
- [Early launch checklist](docs/early-launch-checklist.md)

Verify local deployment readiness before committing:

```powershell
.\scripts\day12_deployment_ready_verify.ps1
```

After manual deployment, run the public smoke check:

```powershell
.\scripts\live_smoke_check.ps1 -BackendUrl "https://your-backend.onrender.com" -FrontendUrl "https://your-frontend.vercel.app"
```

Do not include secrets in Git. `DATABASE_URL`, `SECRET_KEY`, Razorpay secrets and webhook secrets belong only in the Render backend environment. Vercel should receive only the public frontend setting:

```text
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com/api/v1
```

Real payment mode and real AI provider calls are intentionally not enabled in the early live version.

## Run the frontend locally

Start the backend in one PowerShell window. From the project root, install and run the frontend in another:

```powershell
.\scripts\install_frontend.ps1
.\scripts\run_frontend.ps1
```

Open `http://127.0.0.1:5173`. The committed `.env.example` targets the local FastAPI `/api/v1` base URL. No frontend `.env` or secret is committed.

Verify the foundation without starting a browser:

```powershell
.\scripts\day7_frontend_foundation_verify.ps1
```

Populate the local dashboard through authenticated APIs after starting the backend:

```powershell
.\scripts\db_seed_pricing.ps1
.\scripts\seed_demo_data_via_api.ps1
```

Demo login: `demo@outcomeiq.local` / `Demo@12345`. These credentials are synthetic and local-only.

After login, open `/demo-guide` for the presentation sequence, setup commands and simulated-scope disclosure.

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
58 passed
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

### Final report and presentation assets

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
- React authentication, project, dashboard and recommendation pages are implemented
- Verify the frontend foundation with `.\scripts\day7_frontend_foundation_verify.ps1`
- Recharts cost/outcome visuals and the five-run API demo seed are implemented
- Run the opt-in demo verification with `.\scripts\day7_dashboard_charts_verify.ps1`
- The presentation-ready app shell and protected Demo Guide are implemented
- Verify frontend polish with `.\scripts\day8_frontend_polish_verify.ps1`
- The three-service Docker local production-like stack is implemented
- Verify it with `.\scripts\docker_verify.ps1`
- Live-quality host and Docker gates are implemented
- Deterministic demo data is available through `.\scripts\db_seed_demo.ps1`
- Placeholder production environment examples and `.\scripts\pre_deploy_check.ps1` are implemented
- Render/Vercel guidance, the deployment checklist, one-month cost plan and public smoke-check script are implemented
- Final go-live, rollback, troubleshooting and launch-note documentation is implemented
- Next deployment step: manually deploy the simulated-provider MVP and run `.\scripts\prod_smoke_check.ps1`
- Next milestone: final report, architecture diagrams and presentation assets
- Real provider calls, billing sync and autonomous decisions remain deferred

Continue with the [Render and Vercel deployment guide](docs/render-deployment-guide.md). Never commit private `.env` files, store provider secrets, or persist raw prompts/responses.
