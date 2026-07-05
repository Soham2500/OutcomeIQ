# OutcomeIQ — Accelerated MVP Timeline

## Original Three-Month Plan

- **Month 1:** Backend foundation, persistence, authentication and workflow telemetry
- **Month 2:** Analytics, outcome economics and recommendation foundation
- **Month 3:** Deployment, testing, documentation and final demonstration

## New Compressed MVP Plan

### Week 1 — Evidence backend

- FastAPI/PostgreSQL foundation
- Authentication, organizations and projects
- Workflow logging and run traces
- Deterministic cost calculation
- Outcome Contracts and verified run outcomes
- Cost per successful outcome
- Dashboard analytics APIs

### Week 2 — Product surface

- Evidence-backed recommendation API foundation — implemented
- Failure-waste and configuration-comparison rules
- Frontend dashboard foundation consuming stable analytics and recommendation APIs — implemented
- Core loading, empty and error states — implemented
- Evidence-focused cost/outcome charts — implemented
- Repeatable five-run API demo data flow — implemented
- Presentation-ready frontend shell and evaluator Demo Guide — implemented

Next: final report and presentation assets.

### Week 3 — Delivery engineering

- Docker local production-like setup — implemented
- Environment/security review
- Integration and regression testing
- Reproducible synthetic demo data
- End-to-end acceptance scripts
- Live-quality host and Docker gates — implemented
- Deterministic, idempotent presentation dataset — implemented
- Production environment examples and pre-deploy gate — implemented
- Render/Vercel deployment guide and deployment checklist — implemented
- One-month cost plan and public production smoke tooling — implemented
- Final deployment runbook and evidence-based go-live checklist — implemented
- Manual rollback, production troubleshooting and launch-note package — implemented

Next deployment step: perform the manual Render/Vercel deployment with simulated AI telemetry, then run the public production smoke check. No real AI-provider key is needed initially.

Deployment references: `docs/deployment-runbook.md`, `docs/final-go-live-checklist.md`, `docs/rollback-checklist.md`, `docs/production-troubleshooting.md` and `docs/launch-notes-template.md`.

### Week 4 — Academic and interview package

- Final report and architecture diagrams
- Research framing and evaluation results
- Presentation deck
- Demo video
- README, screenshots and portfolio polish

## Scope Constraint

This compressed timeline is possible only if scope stays MVP-focused. Defer real provider billing integrations, autonomous routing, advanced ML forecasting, enterprise SSO/chargeback, multi-cloud allocation and production-scale optimization until the core proof is stable and demonstrated.

Real AI APIs remain deferred until token limits, monthly budget caps, approved model allowlists, complete call logging and a provider kill switch exist.
