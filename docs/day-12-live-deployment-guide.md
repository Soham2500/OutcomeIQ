# Day 12 Live Deployment Guide

OutcomeIQ early live deployment target:

- Backend: Render Web Service
- Database: Render PostgreSQL
- Frontend: Vercel
- Payments: subscription-ready test mode only
- Real payments: not enabled yet

## Part A: Prepare GitHub

1. Run the deployment readiness verification:

```powershell
.\scripts\day12_deployment_ready_verify.ps1
```

2. Check Git status:

```powershell
git status --short
```

3. Review the diff and confirm no `.env` files or secrets appear.
4. Commit only safe files.
5. Push to GitHub.

## Part B: Create Render PostgreSQL

1. Open Render.
2. Create a PostgreSQL database.
3. Copy the internal database URL.
4. Save database details securely.
5. Do not paste the database URL into frontend or Git-tracked files.

## Part C: Deploy Backend on Render

1. Create a Render Web Service from the GitHub repository.
2. Use the backend Dockerfile path through the included `render.yaml`, or configure manually with:
   - Root directory: `backend`
   - Dockerfile: `backend/Dockerfile` if configured from repo root, or `Dockerfile` if root is `backend`
   - Health check path: `/api/v1/health`
3. Set backend environment variables from [render-vercel-env-vars.md](render-vercel-env-vars.md).
4. Deploy.
5. Open:

```text
https://your-backend.onrender.com/api/v1/health
```

Expected health response status is `ok`.

## Part D: Run Migrations and Seed Data

Use one of these options:

- Render shell
- Render one-off job if available
- Local command against the production database only if you are certain the URL is correct and safe

Commands from the backend working directory:

```powershell
alembic upgrade head
python scripts/seed_plans.py
python scripts/seed_pricing_rates.py
```

`seed_plans.py` is required for the Pricing and Billing pages. `seed_pricing_rates.py` is required for simulated demo cost calculation.

## Part E: Deploy Frontend on Vercel

1. Import the GitHub repo into Vercel.
2. Set root directory:

```text
frontend
```

3. Set build command:

```text
npm run build
```

4. Set output directory:

```text
dist
```

5. Add frontend environment variable:

```text
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com/api/v1
```

6. Deploy.

The included `frontend/vercel.json` rewrites all SPA routes to `/index.html`, so refreshes on `/dashboard`, `/pricing` and `/billing` should work.

## Part F: CORS Fix

If the frontend cannot call the backend:

1. Copy the exact Vercel domain.
2. Add it to `BACKEND_CORS_ORIGINS` in Render.
3. Keep local origins only if needed for development.
4. Redeploy the backend.

Example:

```text
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173,http://127.0.0.1:8080
```

## Part G: Live Smoke Test

From the project root:

```powershell
.\scripts\live_smoke_check.ps1 -BackendUrl "https://your-backend.onrender.com" -FrontendUrl "https://your-frontend.vercel.app"
```

Expected final output:

```text
LIVE SMOKE CHECK PASSED
```

## Part H: Manual Functional Test

After smoke test:

1. Register.
2. Login.
3. Create project.
4. Run demo data.
5. Open Dashboard.
6. Open Recommendations.
7. Open Pricing.
8. Activate a test plan.
9. Open Billing.

## Part I: Important Warnings

- Do not enable real payment yet.
- Do not expose secrets.
- Do not commit `.env` files.
- Do not use the production database for random testing after launch.
- Do not call real AI providers in the first live version.
- Keep subscription billing in test/sandbox mode until KYC, policies and webhook verification are complete.
