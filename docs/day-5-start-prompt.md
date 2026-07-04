# Day 5 — Workflow Logging Database Models

You are my senior backend engineer, data architect and database migration mentor.

Project: OutcomeIQ — Outcome-aware AI FinOps Platform

Project root: `C:\Users\soham\OneDrive\Documents\pro`

Current foundation:

- FastAPI modular monolith
- PostgreSQL connected
- Alembic migrations working
- Auth, organization and project APIs complete for the MVP foundation
- Project membership and owner/admin authorization available
- No workflow logging tables or APIs exist yet

Your task is to implement the Day 5 workflow logging database foundation.

Required work:

1. Review `docs/database-design.md`, `docs/system-architecture.md`, existing models, mixins, Alembic revisions and repositories. Do not invent a different architecture.
2. Create only these workflow-related SQLAlchemy models:
   - `Workflow`
   - `WorkflowConfiguration`
   - `WorkflowRun`
   - `ModelCall`
   - `ToolCall`
3. Define clear project/workflow/run foreign keys, UUID primary keys, timezone-aware timestamps, lifecycle/status fields and practical indexes.
4. Represent configuration identity, retry/fallback markers, latency, token usage and raw cost fields without building outcome or recommendation logic.
5. Do not store prompts, responses, API keys, credentials or production customer content.
6. Register only the five approved models with `Base.metadata`.
7. Create one reversible Alembic migration chained from the current head. It must create exactly the five approved tables and drop them in safe reverse dependency order.
8. Extend safe Python and PowerShell scripts to inspect whether all required tables exist. Scripts must never create/drop tables or print secrets.
9. Add tests for model imports, metadata registration and migration discovery. Tests must not require real PostgreSQL or provider APIs.
10. Update verification scripts and Day 5 documentation.

Boundaries:

- Do not create frontend code.
- Do not implement workflow HTTP APIs unless a later prompt explicitly requests them.
- Do not call real AI providers or require API keys.
- Do not implement Outcome Contracts, outcome events or verification.
- Do not implement cost attribution, failure waste, comparisons or recommendations.
- Do not implement autonomous model routing.
- Do not modify or commit `backend/.env`.
- Do not run destructive database commands.
- Do not auto-apply the migration; prepare and validate it for explicit review unless instructed otherwise.

Use simulated/synthetic telemetry examples only. After implementation, confirm the files changed, migration name, tables included, test results, commands to apply/verify the migration and the next recommended Day 5 step.
