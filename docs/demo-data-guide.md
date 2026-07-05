# OutcomeIQ — Deterministic Demo Data Guide

## Purpose

The live-quality demo fixture provides a repeatable AI customer-support dataset for dashboard, unit-economics and recommendation demonstrations. It writes directly through the existing service/repository layer and never calls an external AI provider.

The seed is convergent: stable slugs, configuration versions and external run references prevent uncontrolled duplicate growth. Reruns reuse the same twelve workflow runs and repair/upsert their cost and outcome records.

## Demo Identity and Project

- User: `demo@outcomeiq.local`
- Password: local placeholder `Demo@12345`
- Organization: **OutcomeIQ Demo Org**
- Project: **AI Support Cost Optimization Demo**

The seed never prints the password. These credentials must never be reused outside local demonstration.

## Workflows

1. **Support Ticket Classifier**
2. **Refund Request Assistant**
3. **Escalation Risk Detector**

Each workflow has one deterministic configuration, one Outcome Contract and four runs. Across the project, outcomes include success, failure, escalation and pending verification.

## Expected Dashboard Evidence

The dashboard should show:

- Three workflows and twelve runs
- Multiple calculated model/tool costs
- Successful, failed, escalated and pending outcomes
- Non-zero success rate
- Cost per successful outcome
- Low-cost successes and high-cost unsuccessful attempts

This distribution provides visible failure waste and supports the central OutcomeIQ claim that cheapest per request is not necessarily cheapest per successful outcome.

## Expected Recommendations

The project/workflow recommendation scopes should produce deterministic suggestions such as:

- High failure-rate investigation for workflows with unsuccessful yield
- Cost-per-success tracking before scaling
- Evidence/data-quality guidance when records are incomplete

Recommendations remain suggestions and never modify workflows automatically.

## Commands

Apply migrations and demo pricing before the direct seed:

```powershell
.\scripts\db_migrate.ps1
.\scripts\db_seed_pricing.ps1
.\scripts\db_seed_demo.ps1
```

Run the complete host or Docker gate:

```powershell
.\scripts\live_quality_gate.ps1
.\scripts\live_docker_quality_gate.ps1
```

Docker-only seed:

```powershell
.\scripts\docker_seed_demo.ps1
```

All model/tool telemetry, pricing and outcomes are simulated. No real providers, customers, billing systems or API keys are used.
