# Day 9 Frontend Functional Polish

## Objective

Complete the frontend demo path so OutcomeIQ can be operated from the UI without relying on Swagger for the basic customer-support workflow demonstration.

## What the frontend can now do

- Register and login through the existing authentication flow.
- Create an organization and project with separate organization name, project name and description fields.
- Register workflows from the new Workflows page.
- Run a simulated AI customer-support workflow from Projects, Workflows, Dashboard or Recommendations.
- Automatically create/reuse the demo workflow, workflow configuration and Outcome Contract.
- Record simulated model calls, tool calls, workflow run completion/failure, costs and outcomes.
- Refresh the dashboard to show total runs, total cost, success rate, successful/failed/pending outcomes and cost per successful outcome.
- Generate and dismiss evidence-backed recommendations from the UI.
- Use the Demo Guide page for viva/demo walkthrough steps.

## Pages added or updated

- `frontend/src/pages/ProjectsPage.tsx`
- `frontend/src/pages/WorkflowsPage.tsx`
- `frontend/src/pages/DashboardPage.tsx`
- `frontend/src/pages/RecommendationsPage.tsx`
- `frontend/src/pages/DemoGuidePage.tsx`

## Frontend API clients added

- `frontend/src/api/workflowsApi.ts`
- `frontend/src/api/workflowRunsApi.ts`
- `frontend/src/api/costsApi.ts`
- `frontend/src/api/outcomesApi.ts`
- `frontend/src/api/demoApi.ts`

## Demo scenario flow

The UI demo uses the customer-support ticket:

> My payment failed but money was deducted.

The demo creates or reuses:

- Workflow: `Support Ticket Classifier`
- Workflow configuration: `demo-v1`
- Outcome Contract: `Ticket Resolution Success`
- Simulated pricing for the two local demo models if missing

Then it creates two workflow runs:

1. Run A succeeds, records model/tool telemetry, calculates cost and records a successful outcome.
2. Run B consumes model/tool telemetry, fails the business outcome, calculates cost and records failure waste.

This proves that request cost alone is not enough; companies need cost per successful outcome.

## Run frontend locally

From the project root:

```powershell
.\scripts\run_backend.ps1
```

In another PowerShell window:

```powershell
.\scripts\run_frontend.ps1
```

Open:

```text
http://127.0.0.1:5173
```

## Run Docker app

With Docker Desktop running:

```powershell
.\scripts\docker_verify.ps1
```

Then open:

```text
http://127.0.0.1:8080
```

## Verify frontend build

```powershell
.\scripts\day9_frontend_polish_verify.ps1
```

Expected final output:

```text
DAY 9 FRONTEND POLISH VERIFY PASSED
```

## Intentionally not implemented

- Real AI provider API calls
- Real OpenAI/Anthropic integration
- Advanced dashboard charts on the main Day 9 dashboard
- Production monitoring
- Enterprise UX/role-management polish
- Real cloud billing integration
- Autonomous model routing

The first live-quality MVP remains a simulated-provider demonstration.
