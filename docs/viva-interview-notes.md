# Viva Interview Notes

## What is OutcomeIQ?

OutcomeIQ is an outcome-aware AI FinOps platform that connects AI workflow costs with verified business outcomes.

## What problem does it solve?

It solves the gap between technical AI usage metrics and business success metrics. It helps answer: what did this AI workflow cost per successful outcome?

## What is cost per successful outcome?

It is total workflow cost divided by the number of verified successful outcomes. It is more business-relevant than cost per request.

## Why FastAPI?

FastAPI is fast, typed, beginner-friendly and suitable for modular monolith APIs with automatic Swagger documentation.

## Why PostgreSQL?

PostgreSQL is reliable for relational business data such as users, projects, workflows, telemetry, costs, outcomes and recommendations.

## Why Docker?

Docker helps run the app consistently across local development and production-like environments.

## What APIs are used?

The system exposes REST APIs for auth, organizations, projects, workflows, workflow runs, costs, outcomes, dashboard analytics and recommendations.

## Is real OpenAI API used?

No. The MVP uses simulated provider/model data only. No real AI provider keys are required.

## What is simulated provider pricing?

It is local demo pricing for synthetic model names such as `support-classifier-small` and `support-generator-standard`.

## What is the recommendation engine?

It is a deterministic rule-based engine that reviews cost/outcome metrics and creates human-review recommendations.

## What are limitations?

No real provider calls, no real cloud billing sync, no advanced ML recommendations, no autonomous routing and limited enterprise UX.

## Future scope?

Real provider integrations, cloud billing sync, advanced dashboards, alerts, role-based permissions, CI/CD and ML-based recommendations.

## Approximate live cost for one month?

For a small simulated-provider MVP, cost can remain low using free/low-cost hosting tiers. Real costs depend on chosen database, backend/frontend hosting and traffic. Real AI-provider cost is zero in the current MVP because no real provider is called.
