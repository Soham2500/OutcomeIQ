# OutcomeIQ — Day 6 Dashboard Preparation

## Day 6 Objective

Create read-only dashboard analytics APIs that turn the Day 5 evidence chain into concise project, workflow, cost and outcome summaries. Day 6 should prepare stable backend contracts for a later frontend without building the frontend itself.

## Why a Dashboard Is Needed

OutcomeIQ now records detailed evidence across multiple entities. Operators need a project-level view that answers practical questions quickly: how many workflows ran, what they cost, how many produced verified success, and what each successful outcome cost. Dashboard APIs should aggregate those facts without forcing clients to reconstruct them from raw traces.

## Backend Data Currently Available

- Users and authenticated project memberships
- Organizations
- Projects
- Workflows and versioned configurations
- Workflow runs
- Model calls and tool calls
- Token, latency and retry/fallback telemetry
- Model pricing rates and workflow-run costs
- Outcome Contracts and workflow-run outcomes
- Cost per successful outcome

## Planned Dashboard Views

### Project overview

Project identity, workflow count, run count, recent activity, total calculated cost and high-level outcome totals.

### Workflow runs

Filterable run list with workflow/configuration, technical status, trigger, timing, latency, cost-summary availability and outcome status.

### Run trace

One ordered view of the workflow run, model calls, tool calls, cost summary and verified outcome.

### Cost summary

Total cost, model/tool cost split, token totals, average cost per run and missing/partial cost evidence.

### Outcome summary

Succeeded, failed, escalated, reopened, abandoned, reversed and pending counts plus success rate.

### Cost per successful outcome

Project/workflow/configuration unit economics using the existing deterministic outcome service.

## Day 6 Boundaries

Do not build yet:

- React or any frontend UI
- Advanced ML forecasting or anomaly prediction
- Recommendation engine or automated scale/stop decisions
- Production deployment infrastructure
- Real provider billing/pricing synchronization
- Autonomous model routing
- New aggregate database tables unless a measured performance need is demonstrated

