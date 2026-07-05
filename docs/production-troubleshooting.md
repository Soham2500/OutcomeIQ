# OutcomeIQ — Production Troubleshooting Guide

## Safe Troubleshooting Rules

- Use sanitized service logs and safe HTTP status codes.
- Never paste passwords, access tokens, `SECRET_KEY` or complete database URLs into terminals shared on screen, issues or documentation.
- Change one controlled variable at a time and record the result.
- Run the production smoke check after every fix.
- Roll back when a critical service cannot be restored safely within the launch window.

## 1. Backend Health Does Not Open

Symptoms: `/api/v1/health` times out, returns a 5xx response or the service repeatedly restarts.

Checks:

1. Inspect sanitized build and runtime logs.
2. Confirm the service start command binds to `0.0.0.0` and the platform-provided port when using native Python.
3. Confirm dependencies installed successfully from `backend/requirements.txt`.
4. Confirm `APP_ENV=production` and `DEBUG=false` are syntactically valid.
5. Check that `DATABASE_URL` exists in the hosting environment without printing its value.
6. Compare the deployed commit with the locally verified commit.

Fix the identified configuration/build issue and redeploy. If the new release remains unhealthy, redeploy the previous successful version.

## 2. Frontend Opens but API Requests Fail

Symptoms: the shell loads, but pages show network errors or browser requests target localhost.

Checks:

1. Confirm the production build used `VITE_API_BASE_URL=https://YOUR_BACKEND_DOMAIN/api/v1`.
2. Confirm the backend HTTPS URL is reachable directly.
3. Check browser network status codes without copying tokens.
4. Confirm the frontend origin exactly matches backend `BACKEND_CORS_ORIGINS`.
5. Confirm both services use HTTPS and there is no mixed-content request.

Vite values are compiled at build time. Change the variable and rebuild/redeploy the frontend; restarting an existing static build is insufficient.

## 3. Registration or Login Fails

Checks:

1. Open `/docs` and confirm the auth routes exist.
2. Confirm `/api/v1/ready` reports the database connected.
3. Confirm Alembic migrations are at the expected head revision.
4. Confirm the frontend calls the production `/api/v1` base URL.
5. Inspect sanitized backend status/error logs for the failed request.
6. Use only a synthetic test account and do not print its password or access token.

If the route works in Swagger but not the frontend, focus on frontend base URL/CORS. If both fail, focus on backend/database configuration.

## 4. Dashboard Is Empty

Checks:

1. Confirm a project exists for the authenticated synthetic user.
2. Seed synthetic demo data if this environment is intended for demonstration.
3. Confirm workflow runs include cost records and outcome records.
4. Test the dashboard APIs through `/docs` using a synthetic account.
5. Confirm the selected project ID belongs to the logged-in account.
6. Check whether filters or an empty-state view are hiding valid data.

Do not load real customer data to make the demo look populated.

## 5. Browser Reports a CORS Error

Checks and fix:

1. Copy only the frontend origin, such as `https://YOUR_FRONTEND_DOMAIN`; do not include a route or trailing API path.
2. Set it in backend `BACKEND_CORS_ORIGINS`.
3. Use a comma-separated list only when multiple exact approved origins are required.
4. Redeploy/restart the backend so the environment change takes effect.
5. Retest from a clean browser session.

Do not use wildcard CORS with authenticated endpoints.

## 6. Alembic Migration Fails

Checks:

1. Confirm the private `DATABASE_URL` is present and points to the intended database without printing it.
2. Confirm the deployed working directory contains `alembic.ini` and the migration directory.
3. Confirm the database user has required schema permissions.
4. Inspect the current/head revisions before attempting another migration.
5. Review the exact failed revision and sanitized database error.

Stop automated retries. Do not run a downgrade or edit production tables manually until compatibility and data-loss risks are understood. Use the rollback checklist when the application cannot safely run against the resulting schema.

## 7. A Secret Was Accidentally Committed

1. Stop the deployment and public sharing.
2. Rotate the exposed secret immediately at its issuing system; deleting the line is not enough.
3. Rotate the database password if a connection URL was exposed.
4. Remove the secret from Git history if needed using a reviewed specialist procedure.
5. Force-update remote history only when fully understood and coordinated.
6. Inspect deployment logs, screenshots, artifacts and forks for copies.
7. Update private hosting variables with rotated values and redeploy.
8. Follow `docs/rollback-checklist.md` and document the incident without reproducing the secret.

## Verification After Any Fix

```powershell
.\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
```

Then repeat synthetic registration/login, dashboard and recommendations checks. A smoke pass alone does not prove authenticated product behavior.
