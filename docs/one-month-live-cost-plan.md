# OutcomeIQ — One-Month Live Cost Plan

## Goal

Run OutcomeIQ as a public, presentation-ready MVP website for one month while preserving the evidence workflow and avoiding uncontrolled cloud or AI-provider spend.

## Recommended Setup

| Component | Recommended approach | Cost-control rationale |
|---|---|---|
| Backend | Render Web Service or a similar managed service | One small service with predictable runtime limits |
| Database | Managed PostgreSQL in the same region as the backend | Avoid self-managed database operations and public cross-region traffic |
| Frontend | Render Static Site or Vercel | Static hosting keeps the UI inexpensive and operationally simple |
| AI provider | Simulated provider only | Demonstrates telemetry and outcome economics without provider billing |
| Domain | Optional provider subdomain or a low-cost custom domain | A custom domain improves presentation but is not required for the MVP proof |

## Planning Estimate

Budget approximately **₹1,500 to ₹5,000 for one month** for a minimal demonstration deployment. This is a planning range, not a provider quote. Actual cost depends on current service plans, taxes, region, database retention, bandwidth, custom-domain choices and whether free or trial allowances are available.

Verify current provider prices manually immediately before provisioning. Do not select a plan merely because an older guide labels it free.

## Why the First Version Uses Simulation

The simulated AI provider creates deterministic model/tool telemetry without contacting OpenAI, Anthropic or another paid model API. Consequently:

- there is no model-token bill for the first live month;
- the demo remains repeatable for evaluators;
- no provider key needs to be stored;
- the team can validate OutcomeIQ's cost-per-success product thesis before paying for inference.

Real AI integration can be added later behind an explicit budget and security review.

## Before Enabling Any Real AI API

- Set strict per-request input and output token limits.
- Set a monthly provider budget and alerts below the hard maximum.
- Log every model call, retry and fallback with attributable cost.
- Block expensive models by default and allowlist only approved models.
- Add rate limits and abuse protection to public endpoints.
- Keep provider keys server-side in the hosting platform's secret store.
- Add a kill switch that disables external provider calls without taking the product offline.
- Test failure and retry behavior with synthetic inputs before public access.

## One-Month Operating Controls

- Review service and database usage at least twice each week.
- Keep only synthetic demo data and apply a simple retention policy.
- Disable unused preview deployments and duplicate services.
- Configure provider budget notifications where available.
- Preserve a working rollback commit and database backup expectation.
- Shut down or downgrade the environment after the one-month demonstration unless an extension is approved.

No exact Render, Vercel, database or domain price is asserted here because provider pricing changes. The deployment owner should record the selected plans and final monthly ceiling before creating paid resources.
