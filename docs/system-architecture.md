# OutcomeIQ — MVP System Architecture Document

**Project:** OutcomeIQ — Outcome-aware AI FinOps Platform  
**MVP vertical:** AI customer-support ticket resolution  
**Architecture style:** Modular monolith  
**Duration:** 3 months  
**Primary proof:** The cheapest workflow per attempt may not be the cheapest per successful outcome.

---

## 1. Architecture Overview

OutcomeIQ will be a cloud-deployed web application that receives simulated AI workflow events, connects execution costs to verified support-ticket outcomes and produces evidence-backed economic recommendations.

The MVP should use a **modular monolith**, not microservices. FastAPI will expose one backend application divided into clearly separated domain modules. This provides industry-style separation without the deployment and debugging overhead of distributed services.

### Core architecture principles

1. **PostgreSQL is the financial source of truth.**
2. **Financial calculations are deterministic.**
3. **Outcome verification is separate from technical completion.**
4. **Every cost links to an execution event and applicable rate.**
5. **Every recommendation links to calculated evidence.**
6. **Historical runs retain their contract, configuration and rate context.**
7. **Unknown or unattributed values remain explicitly unknown.**
8. **Sensitive prompt and customer content is not required.**
9. **Simulated model events replace real AI-provider integrations initially.**
10. **Modules are logically separated but deployed as one backend.**

### Selected stack

| Area | Technology |
|---|---|
| Frontend | React, Tailwind CSS |
| Visualisation | Recharts or Chart.js |
| Backend | FastAPI |
| Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Cache/future jobs | Redis |
| Analytics | Python, Pandas |
| Data science | Scikit-learn |
| Local deployment | Docker Compose |
| Frontend hosting | Vercel |
| Backend hosting | Render or Railway |
| Production database | Supabase PostgreSQL |
| Initial monitoring | Structured application logging |
| Future monitoring | Prometheus and Grafana |

---

## 2. High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         OutcomeIQ Users                             │
│ AI Engineer │ Product Manager │ FinOps User │ Project Evaluator    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  React + Tailwind Frontend                          │
│                                                                     │
│ Login │ Project Setup │ Workflow Registry │ Outcome Contracts       │
│ Run Explorer │ Cost Dashboard │ Configuration Comparison            │
│ Failure Waste │ Evidence-backed Recommendations                     │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ REST API / JWT
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FastAPI Modular Monolith                         │
│                                                                     │
│  ┌──────────────────── API and Validation Layer ─────────────────┐  │
│  │ Authentication │ Authorization │ Request Validation │ CORS     │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
│                               ▼                                     │
│  ┌────────────────────── Domain Services ─────────────────────────┐ │
│  │ Auth │ Organizations │ Projects │ Workflows │ Contracts         │ │
│  │ Providers │ Configurations │ Runs │ Calls │ Outcomes │ Audit    │ │
│  └────────────────────────────┬────────────────────────────────────┘ │
│                               ▼                                     │
│  ┌──────────────── Economic and Analytics Services ───────────────┐ │
│  │ Cost Attribution │ Unit Economics │ Failure Waste               │ │
│  │ Configuration Comparison │ Recommendation Engine               │ │
│  └────────────────────────────┬────────────────────────────────────┘ │
│                               ▼                                     │
│  ┌──────────────────── Data Access Layer ─────────────────────────┐ │
│  │ SQLAlchemy Repositories │ Transactions │ Tenant Scoping         │ │
│  └────────────────────────────┬────────────────────────────────────┘ │
└───────────────────────────────┼─────────────────────────────────────┘
                                │
               ┌────────────────┴─────────────────┐
               ▼                                  ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│ Supabase PostgreSQL           │   │ Redis                         │
│                               │   │                               │
│ Users and memberships         │   │ Short-lived dashboard cache  │
│ Workflows and contracts       │   │ Rate limiting/locks later    │
│ Runs, calls and outcomes      │   │ Background jobs later        │
│ Costs and evidence            │   │                               │
└───────────────────────────────┘   └───────────────────────────────┘
               ▲
               │ Simulated telemetry
┌──────────────┴──────────────────────────────────────────────────────┐
│              Simulated AI Customer-Support Workflow                │
│                                                                     │
│ Ticket → Model Call → Payment Tool → Retry → Fallback → Outcome     │
└─────────────────────────────────────────────────────────────────────┘

Deployment:
React → Vercel
FastAPI → Render/Railway
PostgreSQL → Supabase
Redis → Render/Railway-managed Redis or equivalent
```

---

## 3. Main System Components

### 3.1 Frontend dashboard

The frontend provides the complete user-facing workflow.

Responsibilities:

- Authentication screens
- Organization and project selection
- Workflow and configuration management
- Outcome Contract editor
- Workflow run timeline
- Unit-economics dashboard
- Failure-waste analysis
- Configuration comparison
- Recommendation evidence display

Recharts is recommended because it integrates naturally with React. The MVP should use a small number of charts:

- Cost trend
- Outcome distribution
- Failure-waste breakdown
- Configuration comparison

### 3.2 Authentication module

Manages:

- Registration
- Login
- Password verification
- JWT creation and validation
- Session or refresh-token lifecycle
- User account status

Authentication confirms identity. Project-level authorization separately determines what the authenticated user may access.

### 3.3 Organization/project module

Provides basic tenant separation.

An organization contains members and projects. Every workflow, contract, run and analytic result belongs to a project.

The MVP needs only simple roles:

- Organization owner
- Project member

Advanced enterprise permissions are unnecessary.

### 3.4 Workflow registry

Stores the business processes monitored by OutcomeIQ.

A workflow includes:

- Name
- Purpose
- Vertical
- Business and technical ownership
- Active status
- Associated Outcome Contracts
- Available configurations

A workflow represents “Payment Support Resolution,” not an individual model request.

### 3.5 Outcome Contract module

Defines how business success is measured.

Responsibilities:

- Define allowed outcome states
- Record success and failure criteria
- Define pending and reversal rules
- Identify the authoritative evidence source
- Version contracts
- Associate every run with a specific contract version

Historical runs must not change when a contract is revised.

### 3.6 Provider/model registry

Maintains simulated providers, models and rate cards.

The initial registry supports manually configured providers such as:

- Simulated Economy Provider
- Simulated Premium Provider

Future providers may include OpenAI, Gemini, Claude and Ollama.

The module stores pricing definitions but does not call external AI providers in the MVP.

### 3.7 Workflow run tracker

Creates and manages one execution record per support ticket.

It tracks:

- Workflow
- Configuration
- External ticket reference
- Contract version
- Start and completion time
- Technical status
- Outcome status
- Execution correlation identifier

The tracker must preserve the distinction between:

- Technical run completion
- Business outcome finalisation

### 3.8 Model-call logger

Records every simulated model invocation.

It captures:

- Associated workflow run
- Provider and model
- Call sequence
- Input and output tokens
- Latency
- Call status
- Retry/fallback relationship
- Applicable rate
- Calculated cost

Prompt and response content should remain optional and redacted.

### 3.9 Tool-call logger

Records external workflow operations such as:

- Payment-status lookup
- Transaction-history lookup
- Refund-policy lookup

It captures status, latency, cost, error category and retry relationship.

### 3.10 Cost calculation engine

Calculates the direct variable cost of every execution component.

Responsibilities:

- Select the effective model rate
- Calculate model-call cost
- Include configured tool cost
- Aggregate component cost into run cost
- Classify cost as exact, estimated or unattributed
- Prevent double counting
- Preserve calculation evidence

It should not use an LLM or probabilistic model for authoritative calculation.

### 3.11 Outcome reconciliation engine

Connects technical execution with the eventual business outcome.

It manages:

- Success
- Failure
- Pending
- Abandoned
- Reversed

The engine validates permitted state changes. For example, a successful ticket may later become reversed if reopened during the contract’s reversal window.

### 3.12 Unit economics engine

Calculates:

- Cost per attempt
- Success yield
- Cost per successful outcome
- Attribution coverage
- Average outcome latency
- Cost by model, configuration and ticket category

It must display its numerator, denominator, filters and time period.

### 3.13 Failure-waste engine

Classifies expenditure that did not contribute to the accepted outcome.

Initial waste categories:

- Failed model call
- Failed tool call
- Retry caused by failure
- Superseded model response
- Unsuccessful workflow
- Unproductive fallback

The engine should avoid labelling every earlier step as waste merely because a fallback occurred. Waste must link to explicit evidence or a transparent rule.

### 3.14 Configuration comparison engine

Compares two configurations under reasonably similar conditions.

Comparison dimensions:

- Evaluation period
- Ticket category
- Attempt count
- Finalised outcomes
- Cost per attempt
- Success yield
- Cost per successful outcome
- Failure-waste percentage
- Outcome latency
- Attribution coverage

The engine must display sample sizes and avoid conclusions when insufficient data is available.

### 3.15 Recommendation engine

Produces:

- Scale
- Keep
- Optimise
- Investigate
- Restrict
- Stop

For the MVP, this should be a deterministic rule engine.

Every recommendation stores:

- Applied rule version
- Comparison period
- Sample size
- Supporting metrics
- Confidence or sufficiency status
- Human-readable explanation

Scikit-learn may later support anomaly or success prediction, but it should not determine the authoritative recommendation initially.

### 3.16 Analytics dashboard

The dashboard combines results from the economics and comparison engines.

Recommended views:

1. Project overview
2. Workflow economics
3. Run explorer
4. Failure-waste analysis
5. Configuration comparison
6. Recommendation evidence

Avoid building separate CFO, engineering and product dashboards during the MVP.

### 3.17 Audit logging module

Records significant actions such as:

- Login activity
- Workflow changes
- Outcome Contract changes
- Rate changes
- Outcome updates
- Reversals
- Recommendation generation
- Manual outcome verification

Audit logs are different from application error logs and should not contain secrets or sensitive prompt content.

---

## 4. Data Flow

### Example ticket

> “My payment failed but money was deducted.”

### 4.1 Workflow initiation

1. The simulated customer-support system receives the ticket.
2. It selects the “Payment Support Resolution” workflow.
3. It selects Configuration A: Economy-first.
4. The backend creates a workflow run.
5. The run is linked to the active Outcome Contract version.
6. A correlation identifier is assigned for end-to-end traceability.

### 4.2 Primary model call

1. The workflow emits a simulated economy-model call.
2. The model-call logger records tokens, latency and status.
3. The cost engine selects the model rate effective at call time.
4. The call cost is calculated and linked to the run.
5. The model decides that payment status must be checked.

### 4.3 Payment-status tool call

1. The workflow logs a payment-service request.
2. The first tool call times out.
3. The tool logger records failure status, latency and direct cost.
4. The failure-waste engine marks the failed tool call as a waste candidate.

### 4.4 Retry

1. The workflow retries the payment-status tool.
2. The retry references the failed call as its parent.
3. The second call succeeds.
4. The transaction is found in a pending-settlement state.
5. Its cost is added to the run envelope.

### 4.5 Economy-model follow-up

1. A second economy-model call prepares a customer response.
2. The simulated response fails the Outcome Contract’s quality rule.
3. The call remains part of the execution history.
4. Because the response is rejected and superseded, its cost is classified as failure waste.

### 4.6 Fallback-model call

1. The workflow invokes the premium fallback model.
2. The fallback call references the rejected economy-model call.
3. Tokens, latency and cost are recorded.
4. The premium response passes the quality rule.
5. A refund-policy tool confirms the expected reversal period.

### 4.7 Technical completion

1. The workflow sends the accepted response.
2. The run becomes technically completed.
3. The associated business outcome initially becomes pending during the 48-hour verification period.

### 4.8 Outcome recording

1. The ticket remains closed and is not escalated.
2. The authoritative ticket outcome is recorded as success.
3. The outcome event identifies its verification source.
4. If the ticket later reopens, a reversal event is added rather than overwriting history.

### 4.9 Cost envelope calculation

The cost engine aggregates:

- Economy-model calls
- Premium fallback
- Payment tool and retry
- Refund-policy tool
- Any direct workflow compute cost

It separately reports:

- Attributed cost
- Estimated cost
- Unattributed cost
- Attribution coverage

### 4.10 Dashboard update

The analytics service recalculates:

- Cost per attempt
- Success yield
- Cost per successful outcome
- Failure waste
- Configuration-level totals

Redis may invalidate or refresh a short-lived dashboard cache.

### 4.11 Recommendation generation

After sufficient runs exist:

1. The comparison engine compares Economy-first with Quality-first.
2. It verifies comparable periods and ticket categories.
3. The recommendation engine applies deterministic rules.
4. Quality-first is recommended for scaling if it has lower cost per verified success despite higher cost per attempt.
5. Every supporting metric is preserved as recommendation evidence.

---

## 5. Layered Architecture

### 5.1 Presentation layer

**Technology:** React, Tailwind CSS, Recharts

Responsibilities:

- User interaction
- Form validation feedback
- Navigation
- Dashboard rendering
- Run timelines
- Comparison and recommendation presentation

It should not perform authoritative financial calculations.

### 5.2 API layer

**Technology:** FastAPI and Pydantic

Responsibilities:

- REST interface
- Authentication enforcement
- Request validation
- Project context validation
- Error translation
- Response formatting
- Correlation identifiers
- CORS enforcement

### 5.3 Service layer

Contains the product’s business rules:

- Contract versioning
- Run lifecycle
- Cost attribution
- Outcome transitions
- Unit economics
- Waste classification
- Comparison rules
- Recommendation logic

This is the core of OutcomeIQ.

### 5.4 Data access layer

**Technology:** SQLAlchemy and Alembic

Responsibilities:

- Persistence
- Queries
- Transactions
- Project-level scoping
- Repository abstractions
- Database migration management

API routes should not contain direct database logic.

### 5.5 Analytics layer

**Technology:** Python, Pandas and optionally Scikit-learn

Responsibilities:

- Aggregations
- Cohort preparation
- Configuration comparison
- Failure-waste summaries
- Basic anomaly detection
- Future predictive experiments

Pandas is suitable for MVP analysis volumes. Large-scale distributed processing is unnecessary.

### 5.6 Storage layer

**Primary:** PostgreSQL  
**Supporting:** Redis

PostgreSQL stores authoritative operational and financial evidence. Redis stores temporary or reproducible data only.

Redis must not become the sole location for:

- Costs
- Outcomes
- Contracts
- Recommendations
- Audit evidence

### 5.7 Deployment layer

Responsibilities:

- Container packaging
- Environment separation
- Secret configuration
- HTTPS hosting
- Database connectivity
- Basic health monitoring
- Production migrations

---

## 6. Backend Service Architecture

All services live inside one FastAPI deployment.

| Service | Responsibility | Main inputs | Main outputs |
|---|---|---|---|
| `auth_service` | Register users, verify credentials and manage JWT lifecycle | Credentials, token, account context | Authenticated identity, access token, authentication errors |
| `organization_service` | Manage organizations and membership | User identity, organization details, membership action | Organization records and membership decisions |
| `project_service` | Create projects and enforce project access | Organization context, user identity, project details | Project context or authorization rejection |
| `workflow_service` | Manage workflows and configurations | Project, workflow metadata, configuration definitions | Workflow/configuration records and active versions |
| `outcome_contract_service` | Define, validate and version Outcome Contracts | Workflow, outcome rules, verification source, finalisation rules | Valid contract version or validation failure |
| `provider_service` | Manage providers, models and rate cards | Provider/model metadata and effective pricing | Model registry entries and applicable rate |
| `run_tracking_service` | Create runs and track model/tool execution events | Workflow, configuration, ticket reference, call events | Run state, call history and correlation context |
| `cost_calculation_service` | Calculate component and run costs with attribution | Calls, token counts, rates, tool costs | Cost entries, run totals, coverage and calculation evidence |
| `outcome_service` | Record and reconcile business outcomes | Run, outcome state, verification source, timestamp | Valid outcome history and current outcome status |
| `analytics_service` | Calculate unit economics, waste and comparisons | Runs, costs, outcomes, filters and cohorts | Economic metrics, waste summaries and configuration comparisons |
| `recommendation_service` | Apply versioned decision rules to analytic evidence | Comparison result, thresholds, sample sufficiency | Recommendation, confidence status and evidence links |
| `audit_service` | Record security-sensitive and business-significant actions | Actor, project, action, target and metadata | Append-only audit event |

### Service interaction rule

Services may call other services through explicit application interfaces. They should not modify another module’s data directly.

For example:

- `outcome_service` records an outcome.
- `analytics_service` recalculates relevant metrics.
- `recommendation_service` consumes the comparison result.
- `audit_service` records the important state changes.

---

## 7. Database Responsibility Map

This section maps logical data ownership without specifying columns, keys or constraints.

| Module | Data responsibility |
|---|---|
| Authentication | Users, password identities, sessions or refresh-token metadata |
| Organizations | Organizations and user memberships |
| Projects | Projects, project ownership and project membership |
| Workflow registry | Workflow definitions, workflow versions and lifecycle status |
| Outcome Contracts | Contract definitions, versions, outcome rules and verification requirements |
| Provider registry | Providers, models and pricing rate cards |
| Workflow configurations | Named configurations, model roles and active periods |
| Run tracking | Workflow runs, technical states and run-status history |
| Model logging | Model calls, token usage, latency and execution status |
| Tool logging | Tools, tool calls, errors, latency and direct cost |
| Retry/fallback tracking | Parent-child attempt relationships and fallback reasons |
| Cost calculation | Cost entries, attribution types, rate evidence and calculation versions |
| Outcomes | Outcome events, verification source and reversal history |
| Failure waste | Waste classifications, associated execution events and cost evidence |
| Analytics | Optional metric snapshots and comparison results |
| Recommendations | Recommendation category, rule version, supporting metrics and evidence |
| Audit | Actor, action, target, timestamp and safe metadata |

### Data ownership principle

Operational evidence should be stored once and referenced by analytics. Do not copy token or cost values into multiple independent sources that can disagree.

---

## 8. API Responsibility Map

No detailed routes or payloads are required yet.

| API group | Responsibilities |
|---|---|
| Authentication APIs | Registration, login, logout, token refresh and current-user identity |
| Organization APIs | Organization creation, listing and membership management |
| Project APIs | Project creation, listing, selection and member access |
| Workflow APIs | Workflow creation, update, activation and retrieval |
| Outcome Contract APIs | Contract creation, versioning, activation and history |
| Provider/model APIs | Provider, model and rate-card management |
| Configuration APIs | Workflow configuration creation, activation and comparison eligibility |
| Run APIs | Run creation, status update, listing and timeline retrieval |
| Model-call APIs | Simulated model-call event ingestion and retrieval |
| Tool-call APIs | Tool execution event ingestion and retrieval |
| Outcome APIs | Outcome recording, verification, transition and reversal |
| Cost APIs | Run-cost calculation, attribution breakdown and recalculation |
| Analytics APIs | Unit economics, waste summaries and filtered trends |
| Comparison APIs | Two-configuration comparison and cohort details |
| Recommendation APIs | Recommendation generation, current result and evidence retrieval |
| Audit APIs | Authorised audit-event retrieval |
| System APIs | Health, readiness and application-version information |

### API design principle

Telemetry ingestion and dashboard retrieval should remain separate concerns:

- Ingestion records evidence.
- Analytics reads and evaluates evidence.

---

## 9. Security Architecture

### 9.1 Password hashing

Passwords must never be stored directly.

Use:

- Argon2id where practical
- Bcrypt as an acceptable alternative
- Salted adaptive hashing
- Minimum password requirements

Password hashes must never appear in logs or API responses.

### 9.2 JWT authentication

Use short-lived signed access tokens.

JWT claims should identify:

- User
- Token type
- Expiration
- Issuer
- Optional token identifier

Long-lived refresh credentials, if used, should be revocable and handled separately.

### 9.3 Project-level authorization

Every protected query must confirm:

1. The user is authenticated.
2. The resource belongs to a project.
3. The user belongs to the project or its organization.
4. The requested action is permitted.

Frontend hiding is not authorization. Enforcement belongs in the backend.

### 9.4 Environment variables

Store externally:

- JWT signing secret
- Database connection string
- Redis connection string
- Allowed frontend origin
- Environment name
- Future AI-provider credentials

Do not commit secrets to GitHub or Docker images.

### 9.5 API validation

FastAPI/Pydantic should validate:

- Required fields
- Allowed outcome states
- Non-negative tokens and costs
- Valid timestamps
- Valid state transitions
- Project ownership
- Reasonable input sizes

Duplicate telemetry should be handled with idempotency or stable event identifiers.

### 9.6 Sensitive-content redaction

By default, store:

- Ticket reference
- Ticket category
- Model and tool metrics
- Redacted error category
- Outcome evidence type

Avoid storing:

- Payment card data
- Bank details
- Authentication tokens
- Full customer messages
- Complete prompts and responses
- Provider secrets

The demo ticket should use synthetic data.

### 9.7 Audit logs

Audit records should cover:

- Contract changes
- Model-rate changes
- Outcome verification
- Outcome reversal
- Recommendation generation
- Manual recalculation
- Membership changes

Audit logs should be append-oriented and protected from ordinary edits.

### 9.8 Additional MVP controls

- HTTPS in production
- Restricted CORS origins
- Database TLS
- Safe error messages
- Basic request-size limits
- Dependency version management
- Separate development and production configuration

---

## 10. Scalability Architecture

### MVP scale

The initial architecture can support:

- One backend instance
- One PostgreSQL database
- One Redis instance
- Thousands of simulated workflow runs
- Synchronous calculation after event recording
- Cached dashboard summaries
- Small Pandas analysis jobs

This is sufficient for a final-year demonstration.

### PostgreSQL as the core platform

PostgreSQL should handle:

- Transactional workflow data
- Cost evidence
- Outcome history
- Project isolation
- Aggregated analytics at MVP volume

Appropriate indexing can be introduced around project, workflow, configuration, run and time-period queries without changing the architecture.

### Redis in the MVP

Use Redis conservatively for:

- Short-lived dashboard caching
- Cache invalidation markers
- Optional rate limiting
- Optional calculation locks

Redis should not store authoritative financial information.

### Future asynchronous processing

As volume increases, move expensive operations to background workers:

- Cost-envelope recalculation
- Large comparison jobs
- Recommendation regeneration
- Export generation
- Anomaly detection

The frontend can then display job progress rather than waiting for synchronous completion.

### Future event-based ingestion

At higher scale, model and tool calls can be ingested as events:

```text
Workflow event
      ↓
Event ingestion
      ↓
Durable queue
      ↓
Validation and enrichment
      ↓
PostgreSQL
      ↓
Analytics update
```

A message broker is unnecessary for the MVP.

### Future materialized views

PostgreSQL materialized views or summary tables may later accelerate:

- Daily workflow economics
- Configuration comparisons
- Waste breakdowns
- Organization-wide summaries

The underlying execution evidence remains authoritative.

### Future horizontal scale

FastAPI can later run multiple stateless instances behind a load balancer. JWT validation and PostgreSQL-backed state make this possible without redesigning the product.

---

## 11. Observability Architecture

### 11.1 Backend application logs

Record:

- Timestamp
- Log severity
- Environment
- Request correlation identifier
- Project and run identifier where safe
- Module
- Event type

Do not log secrets, tokens or customer text.

### 11.2 Request logs

Capture:

- HTTP method
- Route group
- Status
- Duration
- Correlation identifier

Avoid logging complete authentication or telemetry payloads.

### 11.3 Error logs

Record:

- Error category
- Safe context
- Stack trace in protected environments
- Correlation identifier
- Affected run or calculation

User-facing responses should not expose stack traces.

### 11.4 Audit logs

Audit logs explain who changed business-relevant state. Application logs explain what the software did. They must remain separate.

### 11.5 Cost calculation traceability

Every calculated cost should be traceable to:

- Execution event
- Provider/model or tool
- Usage quantity
- Effective rate
- Calculation version
- Attribution classification
- Calculation timestamp

This is more important than advanced monitoring for the MVP.

### 11.6 Recommendation traceability

Every recommendation should preserve:

- Rule version
- Comparison cohort
- Sample size
- Input metrics
- Thresholds
- Result
- Insufficient-evidence conditions

A recommendation must be reproducible from stored evidence.

### 11.7 Future Prometheus/Grafana

Future operational metrics may include:

- Request rate
- Error rate
- API latency
- Database latency
- Cache hit rate
- Calculation failures
- Queue depth
- Recommendation-generation duration

Prometheus and Grafana should be introduced only after the core product works.

---

## 12. Deployment Architecture

### 12.1 Local development

Use Docker Compose with:

- React frontend
- FastAPI backend
- PostgreSQL
- Redis

Local services should use development-only credentials and synthetic data.

### 12.2 Production deployment

```text
User Browser
     │
     ▼
Vercel
React + Tailwind
     │ HTTPS
     ▼
Render or Railway
FastAPI backend
     │
     ├──────── TLS ────────► Supabase PostgreSQL
     │
     └────────────────────► Managed Redis
```

### 12.3 Frontend on Vercel

Responsibilities:

- Build React application
- Serve static assets
- Inject public backend URL
- Provide HTTPS
- Support environment-specific configuration

No private secret should be embedded in the frontend.

### 12.4 Backend on Render/Railway

Responsibilities:

- Run FastAPI application
- Execute migrations during controlled deployment
- Access PostgreSQL and Redis
- Expose health/readiness checks
- Store private environment variables

### 12.5 Database on Supabase

Use Supabase as managed PostgreSQL.

The backend should connect directly through a secure database connection. Supabase-specific features are optional; OutcomeIQ should remain compatible with standard PostgreSQL.

### 12.6 Environment variables

Separate configuration for:

- Local development
- Test environment
- Production

At minimum:

- Database connection
- Redis connection
- JWT secret
- Allowed frontend origin
- Application environment
- Logging level

### 12.7 GitHub repository

Recommended top-level separation:

- Frontend application
- Backend application
- Migrations
- Deployment configuration
- Documentation
- Controlled demo assets

Avoid storing production data or secrets in the repository.

### 12.8 CI/CD progression

Initial deployment may remain manual and documented.

Later CI/CD should:

1. Run backend tests.
2. Run frontend checks.
3. Verify migration consistency.
4. Build containers.
5. Deploy approved changes.
6. Run post-deployment health checks.

Kubernetes is unnecessary.

---

## 13. Architecture Risks and Mitigation

| Risk | Likely impact | Mitigation |
|---|---|---|
| Overengineering | Core product remains incomplete | Use a modular monolith, one vertical and one dashboard. Reject microservices and message brokers during MVP. |
| Incorrect cost calculation | Invalid product conclusions | Use deterministic formulas, versioned rates and independent test datasets. Display calculation components. |
| Missing outcome evidence | Artificially optimistic economics | Require verification source and distinguish pending, verified and reversed outcomes. |
| Double counting cost | Inflated workflow totals | Give each cost one source event and one aggregation path. Use idempotent event identifiers. |
| Incorrect waste classification | Useful work is labelled waste | Start with narrow, evidence-backed waste categories and show classification reason. |
| Low sample size | Misleading recommendation | Display sample count, require a minimum threshold and return Investigate when evidence is insufficient. |
| Sensitive-data exposure | Security and privacy failure | Use synthetic tickets, redact prompts and prohibit payment information and secrets. |
| Complex deployment | Time lost on infrastructure | Use Vercel, Render/Railway and Supabase; keep Docker Compose for local development. |
| Unreliable recommendation logic | Users cannot trust decisions | Use deterministic, versioned rules and preserve all numerical evidence. |
| Rate changes alter history | Historical metrics become inconsistent | Select rates by execution time and retain the applied rate reference. |
| Pending outcomes distort metrics | Success yield becomes inaccurate | Separate technical completion from outcome finalisation and exclude pending results from finalised denominators. |
| Redis inconsistency | Cached values disagree with PostgreSQL | Treat PostgreSQL as authoritative and make cached values disposable. |
| Frontend performs calculations | Different screens show different values | Perform all authoritative economics calculations in the backend. |
| Excessive AI use | Hallucinated financial analysis | Use AI only for optional explanation; calculations and decisions remain deterministic. |
| Scope growth | Three-month delivery fails | Freeze must-have acceptance criteria and remove Could Have features first. |

---

## 14. Final Architecture Summary

OutcomeIQ should be built as a React frontend connected to a FastAPI modular monolith, with PostgreSQL as the authoritative store and Redis limited to disposable caching and future background jobs. SQLAlchemy and Alembic provide structured persistence and migration management, while Pandas supports configuration analysis at MVP scale.

This architecture is realistic for three months because it avoids real provider integrations, microservices, Kubernetes, distributed queues and enterprise billing systems. It still appears industry-grade because it includes tenant separation, versioned Outcome Contracts, reproducible costs, outcome history, project-level authorization, auditability and recommendation evidence.

Most importantly, the architecture protects the central product claim: every recommendation can be traced from a verified customer-support outcome back through the workflow configuration, model and tool calls, applicable rates, calculated cost and identified failure waste.
