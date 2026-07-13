# OutcomeIQ — Manual Deployment Runbook

## Purpose

This runbook is the final operator sequence for hosting OutcomeIQ as a one-month public MVP. It coordinates the detailed [Render/Vercel guide](render-deployment-guide.md), [go-live checklist](final-go-live-checklist.md), [rollback checklist](rollback-checklist.md) and [troubleshooting guide](production-troubleshooting.md).

The deployment remains manual. Use placeholders until values are entered directly into the hosting platforms. The first live version uses only simulated AI-provider telemetry and requires no real AI API key.

## Deployment Record

Complete this record outside committed source files if it contains private operational information.

| Field | Value |
|---|---|
| Deployment owner | `<OWNER>` |
| Planned date/time | `<YYYY-MM-DD HH:MM TIMEZONE>` |
| Git commit SHA | `<COMMIT_SHA>` |
| Previous working SHA | `<ROLLBACK_COMMIT_SHA>` |
| Backend host | `<BACKEND_PROVIDER>` |
| Frontend host | `<FRONTEND_PROVIDER>` |

## A. Pre-Deployment

1. Open PowerShell at the project root:

   ```powershell
   cd C:\Users\soham\OneDrive\Documents\pro
   ```

2. Pull the latest reviewed `main` branch manually. Stop if the pull introduces conflicts or unexpected changes.
3. Confirm the current branch, commit SHA and clean working tree:

   ```powershell
   git branch --show-current
   git rev-parse HEAD
   git status --short
   ```

4. Confirm neither `backend/.env` nor `frontend/.env` appears in Git status or repository history.
5. Run the full non-deploying readiness gate:

   ```powershell
   .\scripts\pre_deploy_check.ps1
   ```

6. Confirm the latest Docker verification passed:

   ```powershell
   .\scripts\docker_verify.ps1
   ```

7. Confirm the gate evidence includes passing backend tests and a successful frontend production build.
8. Record the current and previous working commit SHAs. Do not continue without a known rollback target.

Pre-deployment gate: continue only when the working tree is understood, private environment files are protected, and every required check passes.

## B. Backend Deployment

1. Create a managed PostgreSQL database in the same region as the planned backend where practical.
2. Create a backend Web Service from the reviewed GitHub commit using the method in `docs/render-deployment-guide.md`.
3. Set the service root to `backend` when required by the platform.
4. Add these values through the provider's private environment interface:

   ```text
   APP_NAME=OutcomeIQ
   APP_ENV=production
   DEBUG=false
   DATABASE_URL=<MANAGED_POSTGRESQL_URL>
   SECRET_KEY=<LONG_RANDOM_PRODUCTION_SECRET>
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   BACKEND_CORS_ORIGINS=https://YOUR_FRONTEND_DOMAIN
   OPENAI_API_KEY=<OPENAI_API_KEY>
   GEMINI_API_KEY=<GEMINI_API_KEY>
   DEFAULT_AI_PROVIDER=gemini
   DEFAULT_AI_MODEL=gemini-3.5-flash
   DEFAULT_OPENAI_MODEL=gpt-4o-mini
   DEFAULT_GEMINI_MODEL=gemini-3.5-flash
   COST_CURRENCY=INR
   USD_TO_INR_RATE=83.50
   AI_PROVIDER_TIMEOUT_SECONDS=60
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=<GMAIL_ADDRESS>
   SMTP_PASSWORD=<GMAIL_APP_PASSWORD>
   MAIL_FROM=<GMAIL_ADDRESS>
   MAIL_FROM_NAME=OutcomeIQ
   OTP_EXPIRE_MINUTES=10
   OTP_RESEND_COOLDOWN_SECONDS=60
   ```

5. Do not upload `backend/.env` and do not reuse local Docker Compose credentials.
6. Deploy the recorded commit and inspect sanitized build/startup logs.
7. Test the public backend endpoints:

   - `https://YOUR_BACKEND_DOMAIN/api/v1/health`
   - `https://YOUR_BACKEND_DOMAIN/docs`

Stop and troubleshoot if health does not return success. Do not proceed merely because the deployment dashboard says the service is running.

## C. Database Setup

Run these commands from the deployed backend working directory using the hosting platform's approved shell, release job or one-off task:

1. Apply reviewed migrations:

   ```text
   alembic upgrade head
   ```

2. Seed deterministic demo pricing:

   ```text
   python scripts/seed_pricing_rates.py
   ```

3. Seed synthetic demo data only when the public demonstration needs it:

   ```text
   python scripts/seed_demo_data.py
   ```

4. Confirm readiness:

   - `https://YOUR_BACKEND_DOMAIN/api/v1/ready`

Readiness should report a connected database. Never run unreviewed migration downgrades or load real customer data into this MVP.

## D. Frontend Deployment

1. Create the static frontend service from the same reviewed commit.
2. Set the frontend root directory to `frontend` where supported.
3. Configure the public build variable:

   ```text
   VITE_API_BASE_URL=https://YOUR_BACKEND_DOMAIN/api/v1
   ```

4. Build and deploy the static site using the provider settings in `docs/render-deployment-guide.md`.
5. Configure the SPA fallback to `index.html` so direct page loads work.
6. Copy the final frontend HTTPS origin into backend `BACKEND_CORS_ORIGINS`.
7. Redeploy the backend if the CORS environment value changed.
8. Confirm browser network requests use the production backend and never `localhost`.

## E. Post-Deployment Smoke Check

Run the unauthenticated public smoke check from the project root:

```powershell
.\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
```

Continue only when it prints:

```text
PRODUCTION SMOKE CHECK PASSED
```

This checks backend health, API documentation and the frontend homepage. It does not replace authenticated browser verification.

## F. Manual Browser Check

Use only synthetic demonstration credentials and data.

1. Open `https://YOUR_FRONTEND_DOMAIN` in a private browser window.
2. Register a synthetic user or log in with an approved synthetic demo account.
3. Open the projects page and select the demo project.
4. Open the dashboard and confirm cost and outcome data is visible.
5. Confirm cost per successful outcome is visible and understandable.
6. Open the recommendations page and confirm evidence-backed recommendations render.
7. Refresh each protected route to verify the SPA fallback.
8. Check the browser console and network panel for visible errors, localhost calls or exposed secrets.
9. Complete `docs/final-go-live-checklist.md`.

## Go/No-Go Rule

Go live only when every required checklist item passes. If a critical check fails, stop public sharing and follow `docs/rollback-checklist.md`. Record the release using `docs/launch-notes-template.md` without adding secrets.
