# Day 6 — Dashboard Analytics API Foundation

You are my senior backend engineer and analytics API architect.

Project: OutcomeIQ — Outcome-aware AI FinOps Platform

Project root: `C:\Users\soham\OneDrive\Documents\pro`

Current foundation:

- FastAPI modular monolith
- PostgreSQL and Alembic migrations
- Authentication, organizations and projects
- Workflow/configuration/run logging APIs
- Model-call and tool-call telemetry
- Deterministic workflow-run cost calculation
- Outcome Contracts and workflow-run outcomes
- Cost-per-successful-outcome service and API

Your task is to create the Day 6 dashboard analytics API foundation.

Required work:

1. Review the existing models, repositories, services, authorization dependencies, APIs and Day 5 documentation. Preserve the modular-monolith architecture and current behavior.
2. Create read-only dashboard schemas, repositories/services and protected endpoints under `/api/v1/dashboard`.
3. Add a project summary that aggregates workflow count, run count, total cost, outcome counts, success rate and cost per successful outcome.
4. Add workflow-run count summaries grouped by technical status and, where useful, workflow/configuration.
5. Add a cost summary containing calculated run count, missing/partial cost evidence, token totals, model/tool cost and total cost.
6. Add an outcome summary containing succeeded, failed, escalated, reopened, abandoned, reversed and pending counts.
7. Return the existing deterministic cost-per-successful-outcome metric rather than duplicating its formula.
8. Enforce active-user authentication and project-membership boundaries on every dashboard endpoint.
9. Avoid new aggregate tables unless a demonstrated query/performance need requires one.
10. Create database-independent schema, import, arithmetic and route-registration tests.
11. Create `scripts/smoke_dashboard_api.ps1` using synthetic local data. It must assume the backend is already running, never print passwords/tokens and never call real providers.
12. Update verification scripts, README files and create Day 6 dashboard API documentation.

Boundaries:

- Do not create frontend code yet.
- Do not create a recommendation engine yet.
- Do not call real AI providers or add API keys.
- Do not implement real provider billing synchronization.
- Do not modify or commit `backend/.env`.
- Do not commit or push automatically.

After implementation, confirm files changed, endpoints added, test results, backend/smoke commands, deferred work and the next recommended milestone.
