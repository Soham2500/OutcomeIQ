# OutcomeIQ — Final Go-Live Checklist

Use this checklist immediately before making the one-month MVP URL public. A checked item must represent observed evidence, not an assumption.

## Code Readiness

- [ ] GitHub `main` contains the reviewed deployment commit
- [ ] Local working tree is clean or every remaining change is understood and excluded from deployment
- [ ] Deployed commit SHA is recorded
- [ ] Previous working rollback SHA is recorded
- [ ] `backend/.env` is not committed
- [ ] `frontend/.env` is not committed
- [ ] Backend tests pass
- [ ] Frontend production build passes
- [ ] `.\scripts\pre_deploy_check.ps1` passes
- [ ] Latest applicable Docker verification passes

## Backend Readiness

- [ ] Backend service is deployed from the recorded commit
- [ ] Private `DATABASE_URL` is configured in the hosting platform
- [ ] New long random `SECRET_KEY` is configured in the hosting platform
- [ ] `DEBUG=false`
- [ ] `APP_ENV=production`
- [ ] `BACKEND_CORS_ORIGINS` contains the exact frontend HTTPS origin
- [ ] `/api/v1/health` returns success
- [ ] `/api/v1/ready` reports the database connected
- [ ] `/docs` opens
- [ ] Reviewed Alembic migrations are applied
- [ ] Deterministic pricing rates are seeded

## Frontend Readiness

- [ ] `VITE_API_BASE_URL` points to the production backend `/api/v1` URL
- [ ] Frontend build passes with the production variable
- [ ] Static output directory and SPA fallback are configured
- [ ] Login page opens over HTTPS
- [ ] Projects page opens
- [ ] Dashboard page opens and survives direct refresh
- [ ] Recommendations page opens and survives direct refresh
- [ ] Browser requests do not target localhost

## Security Readiness

- [ ] First live version uses the simulated AI provider only
- [ ] No real AI-provider API key is configured
- [ ] No secrets appear in README or other committed documentation
- [ ] No secrets appear in screenshots, demo recordings or browser console output
- [ ] No secrets appear in GitHub commits or deployment logs
- [ ] Local Docker credentials are not reused in production
- [ ] Only synthetic demo accounts and data are present
- [ ] Hosting/database access is limited to the deployment owner

## Demo Readiness

- [ ] Synthetic demo data is seeded if required
- [ ] Dashboard contains visible cost and outcome data
- [ ] Recommendations are visible with numerical evidence
- [ ] Cost per successful outcome is visible
- [ ] Demo explanation and navigation sequence are rehearsed
- [ ] The story demonstrates why the cheapest request is not always the cheapest successful outcome
- [ ] Known limitations are ready to explain
- [ ] Launch notes are prepared from `docs/launch-notes-template.md`

## Final Verification

- [ ] Production smoke check passes:

  ```powershell
  .\scripts\prod_smoke_check.ps1 -BackendBaseUrl "https://YOUR_BACKEND_DOMAIN" -FrontendBaseUrl "https://YOUR_FRONTEND_DOMAIN"
  ```

- [ ] Manual registration/login succeeds with a synthetic account
- [ ] No critical errors remain in backend logs or browser console
- [ ] Rollback checklist and previous working deployment are available

## Final Go-Live Decision

- [ ] **GO:** All required checks pass and the URL may be shared
- [ ] **NO-GO:** One or more required checks failed; keep sharing disabled and troubleshoot or roll back

Go live only if all required checks pass. Never convert a failed critical check into an accepted risk merely to meet a demonstration date.
