# OutcomeIQ — Day 9 Production Environment and Pre-Deploy Checks

## Purpose

Hosting OutcomeIQ for a one-month live demonstration requires a clear separation between committed configuration examples and private deployment values. The production examples document the required contract without containing a usable database credential, signing key or domain.

No deployment is performed by this milestone.

## Backend Production Variables

Copy `backend/.env.production.example` into the chosen hosting platform’s private environment-variable interface. Do not create or commit a populated production file in this repository.

| Variable | Purpose |
|---|---|
| `APP_NAME` | Public application/service name |
| `APP_ENV` | Sets the effective environment to `production` |
| `DEBUG` | Must remain `false` for the live version |
| `DATABASE_URL` | Private SQLAlchemy PostgreSQL connection URL |
| `SECRET_KEY` | Long random JWT signing secret mapped to the backend security setting |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifetime for the demonstration |
| `BACKEND_CORS_ORIGINS` | Exact HTTPS frontend origin or comma-separated approved origins |

In production, the backend uses only explicitly configured CORS origins. Development and Docker environments continue to support their approved localhost origins.

## Frontend Production Variable

Vite compiles its public API base URL during the frontend build:

```text
VITE_API_BASE_URL=https://YOUR_BACKEND_DOMAIN/api/v1
```

The committed `frontend/.env.example` retains the local default and shows the production placeholder as a comment. Do not create or commit `frontend/.env`.

## Secret Safety Rules

- Never commit `backend/.env` or `frontend/.env`.
- Never replace example placeholders with real deployment values.
- Store the database URL and signing key only in the hosting provider’s secret/environment system.
- Use separate local and production credentials.
- Do not place API keys or tokens in Vite variables; Vite variables are visible to browsers.
- Review `git status --short` before every commit.

## Pre-Deploy Check

From the project root, with local PostgreSQL available:

```powershell
.\scripts\pre_deploy_check.ps1
```

The check validates private-file protection, example trackability, backend tests, frontend production build and the complete host live-quality gate. A successful run ends with:

```text
PRE DEPLOY CHECK PASSED
```

The script does not create cloud resources, upload images or deploy services.

## First Live-Version Scope

The first hosted version will continue using simulated model/tool telemetry and deterministic demo pricing. This is intentional: it demonstrates outcome-aware unit economics without real provider keys, customer data or billing access.

## Intentionally Not Done

- Actual Render, Vercel or other cloud deployment
- Real production secrets or domains
- Cloud PostgreSQL creation
- Real AI-provider API keys or calls
- Real billing/provider synchronization
- DNS, HTTPS and monitoring configuration

The provider-specific manual sequence is now documented in `docs/render-deployment-guide.md`, with acceptance criteria in `docs/deployment-checklist.md` and budget guidance in `docs/one-month-live-cost-plan.md`. Actual deployment remains a separate manual step.
