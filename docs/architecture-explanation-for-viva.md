# Architecture Explanation for Viva

## High-level flow

```text
User
  ↓
React Frontend
  ↓
FastAPI Backend
  ↓
Services and Repositories
  ↓
PostgreSQL
  ↓
Dashboard / Recommendation Response
```

The user operates OutcomeIQ from the React frontend. The frontend calls protected FastAPI REST endpoints. The backend validates requests, applies business logic in services, reads/writes PostgreSQL through repositories, and returns dashboard or recommendation responses.

## Outcome-aware workflow flow

```text
Workflow Run
  ↓
Model Calls + Tool Calls
  ↓
Cost Calculation
  ↓
Outcome Tracking
  ↓
Dashboard Analytics
  ↓
Recommendation Generation
```

Each workflow run records simulated model and tool telemetry. The cost service calculates model/tool cost. The outcome service records whether the business result succeeded, failed, escalated or stayed pending. Dashboard analytics then calculate success rate and cost per successful outcome. The recommendation engine uses those metrics to create evidence-backed recommendations.

## Why this architecture fits the MVP

- Modular monolith keeps development simple for a 3-month project.
- PostgreSQL supports strong relational consistency.
- React provides a clean SaaS-style demo surface.
- Docker supports repeatable local production-like execution.
- Simulated provider data avoids security and cost risks while proving the product concept.
