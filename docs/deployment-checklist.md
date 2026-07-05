# OutcomeIQ — Deployment Checklist

Use this checklist for the manual one-month MVP deployment. Record the deployed commit and completion evidence outside the repository without copying credentials.

## Before Deployment

- [ ] Git working tree is clean
- [ ] Intended commit SHA has been reviewed and pushed
- [ ] `backend/.env` is not committed or visible in Git status
- [ ] `frontend/.env` is not committed or visible in Git status
- [ ] `.\scripts\pre_deploy_check.ps1` passes
- [ ] `.\scripts\docker_verify.ps1` passes with Docker Desktop running
- [ ] Frontend production build passes
- [ ] Backend tests pass
- [ ] No real AI-provider key is present or required
- [ ] Rollback commit SHA is recorded

## Backend Production

- [ ] Managed PostgreSQL database is provisioned
- [ ] Private `DATABASE_URL` is set in the hosting platform
- [ ] New long random `SECRET_KEY` is set in the hosting platform
- [ ] `DEBUG=false`
- [ ] `APP_ENV=production`
- [ ] `BACKEND_CORS_ORIGINS` contains the exact frontend HTTPS origin
- [ ] Backend health-check path is `/api/v1/health`
- [ ] Alembic migrations are applied once and verified
- [ ] Deterministic pricing rates are seeded
- [ ] Synthetic demo data is seeded only if desired
- [ ] No local Docker Compose credentials are reused

## Frontend Production

- [ ] `VITE_API_BASE_URL` points to the HTTPS backend `/api/v1` URL
- [ ] Production build completes successfully
- [ ] Static publish/output directory is correct
- [ ] SPA fallback to `index.html` is configured
- [ ] Login page opens
- [ ] Dashboard page opens, including direct navigation/refresh
- [ ] Recommendations page opens, including direct navigation/refresh
- [ ] Browser requests target the production backend rather than localhost

## After Deployment

- [ ] Backend `/api/v1/health` returns success
- [ ] Backend `/docs` opens
- [ ] Frontend homepage opens over HTTPS
- [ ] Synthetic user registration and login work
- [ ] Dashboard loads for the synthetic demo project
- [ ] Recommendations page loads
- [ ] `.\scripts\prod_smoke_check.ps1` passes
- [ ] No secrets are visible in the repository, frontend bundle or browser console
- [ ] Logs contain no access tokens, passwords or database URLs
- [ ] Production database backup/restore expectations are documented
- [ ] Deployed commit SHA and deployment time are recorded

## First Live-Version Boundary

- [ ] AI-provider behavior remains simulated
- [ ] No real provider API key has been configured
- [ ] No customer or sensitive production data has been loaded
- [ ] Human review remains required for recommendations
