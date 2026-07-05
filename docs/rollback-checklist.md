# OutcomeIQ — Manual Rollback Checklist

## Purpose

This is a safety document for restoring the last known working public MVP. It does not implement automatic rollback. Keep the previous successful deployment and commit SHA available before every release.

## Roll Back When

- [ ] Backend health or readiness fails after deployment
- [ ] Frontend cannot load or protected routes consistently fail
- [ ] Registration or login is broken
- [ ] A database migration fails or leaves schema compatibility uncertain
- [ ] CORS prevents the frontend from reaching the backend
- [ ] A secret, credential or private connection URL is exposed
- [ ] The deployed release causes data corruption or repeated server errors
- [ ] Production smoke or required manual browser checks fail

## Immediate Containment

- [ ] Stop sharing the public URL and pause the launch
- [ ] Preserve sanitized logs, timestamps and the failed deployment SHA
- [ ] Disable public access temporarily if exposure or data risk exists
- [ ] Do not print, copy into tickets or commit any exposed secret
- [ ] Do not run an automatic database downgrade

## Code or Configuration Rollback

- [ ] Identify whether the failure is code, configuration, database or frontend-cache related
- [ ] Redeploy the previous successful Render/Vercel deployment or known-good commit
- [ ] Revert the last commit through a reviewed Git change if the defect is in code
- [ ] Restore the previous known-good environment values through the hosting platform if configuration caused the failure
- [ ] Reapply the exact approved frontend origin if CORS caused the failure
- [ ] Confirm frontend `VITE_API_BASE_URL` targets the restored backend

## Database Safety

- [ ] Stop writes if schema or data integrity is uncertain
- [ ] Review the failed Alembic revision and database logs
- [ ] Confirm whether the previous application version is compatible with the current schema
- [ ] Restore from a verified backup only when required and understood
- [ ] Do not run `alembic downgrade` without reviewing data-loss and compatibility risks
- [ ] Record any manual database action and its result

## Secret Exposure Response

- [ ] Stop the affected deployment or disable public access
- [ ] Rotate an exposed `SECRET_KEY`
- [ ] Rotate an exposed database password and update the private `DATABASE_URL`
- [ ] Rotate any other exposed credential at its issuing provider
- [ ] Treat a committed secret as compromised even if the commit is later deleted
- [ ] Remove the secret from Git history if needed using a reviewed history-rewrite procedure
- [ ] Force-update remote history only when the consequences are fully understood and collaborators are coordinated
- [ ] Check screenshots, logs, build artifacts and deployment variables for additional copies

## Verify the Rollback

- [ ] Backend `/api/v1/health` returns success
- [ ] Backend `/api/v1/ready` reports expected dependency state
- [ ] Backend `/docs` opens
- [ ] Frontend opens and no longer calls the failed service URL
- [ ] Synthetic registration/login works
- [ ] Dashboard and recommendations load
- [ ] Production smoke check passes:

  ```powershell
  .\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
  ```

- [ ] Incident, root cause, affected deployment and corrective action are documented without secrets

Public sharing should resume only after the rollback is verified and the security impact, if any, is contained.
