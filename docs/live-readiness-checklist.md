# OutcomeIQ — Live-Readiness Checklist

OutcomeIQ is now treated as a live-quality MVP. Fast delivery remains acceptable only when the relevant quality gates continue to pass.

## 1. Working Status

- [x] FastAPI backend runs locally
- [x] React frontend runs locally
- [x] Local PostgreSQL connectivity and migrations work
- [x] PostgreSQL/backend/frontend Docker stack works locally
- [x] Auth, workflow, cost, outcome, dashboard and recommendation smoke scripts exist
- [x] Deterministic customer-support demo dataset exists
- [x] Host quality gate exists: `.\scripts\live_quality_gate.ps1`
- [x] Docker quality gate exists: `.\scripts\live_docker_quality_gate.ps1`

## 2. Security Status

- [x] `backend/.env` is ignored and must never be committed
- [x] `frontend/.env` is ignored and must never be committed
- [x] Committed credentials are explicitly local demo placeholders only
- [x] No real API keys are required
- [x] No real AI-provider calls occur
- [x] Smoke and verification scripts do not print tokens or private database URLs

Before every commit, verify that neither private environment file appears in `git status --short`.

## 3. MVP Feature Status

- [x] User registration, login and current-user authentication
- [x] Organizations and projects
- [x] Workflow/configuration registry
- [x] Workflow runs and model/tool call logging
- [x] Deterministic cost calculation
- [x] Outcome Contracts and run-outcome tracking
- [x] Cost-per-success and dashboard analytics
- [x] Rule-based, human-reviewed recommendations
- [x] React dashboard, charts and evaluator Demo Guide
- [x] Local Docker Compose setup

## 4. Remaining Before Public Deployment

- [ ] Replace all placeholder credentials with production secrets
- [ ] Add HTTPS and secure reverse-proxy configuration
- [ ] Provision a managed cloud PostgreSQL database
- [ ] Configure production domain and DNS
- [ ] Add CI/CD with protected deployment environments
- [ ] Host frontend and backend in approved infrastructure
- [ ] Add centralized monitoring, alerts and audit retention
- [ ] Define database backup and restore procedures
- [ ] Complete production security, privacy and accessibility review

## 5. Quality Rule

Every milestone must pass the applicable checks:

1. Backend tests
2. Frontend typecheck/build
3. API smoke scripts
4. Private-secret Git check
5. Database migration/table verification
6. Docker or local end-to-end verification where applicable

Primary commands:

```powershell
.\scripts\live_quality_gate.ps1
.\scripts\live_docker_quality_gate.ps1
```

A milestone is not complete merely because it runs once; its fixture and verification paths must remain repeatable.
