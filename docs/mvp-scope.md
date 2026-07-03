# OutcomeIQ — Three-Month MVP Scope Document

**Project:** OutcomeIQ — Outcome-aware AI FinOps Platform  
**MVP vertical:** AI customer-support ticket resolution  
**Duration:** 12 weeks  
**Primary product proof:** The cheapest workflow per attempt may not be the cheapest per successful business outcome.

---

## 1. MVP Goal

The first version of OutcomeIQ must prove that AI workflow cost can be connected to a verified customer-support outcome and used to make a better economic decision.

By the end of three months, the product should:

1. Register a customer-support AI workflow.
2. Define what “successful ticket resolution” means through an Outcome Contract.
3. Track every workflow run.
4. Record model calls, tools, retries and fallbacks.
5. Calculate directly attributable execution cost.
6. Record success, failure, pending, abandoned and reversed outcomes.
7. Calculate outcome-aware unit economics.
8. Identify money consumed by failed or superseded operations.
9. Compare two workflow configurations.
10. Generate a recommendation supported by numerical evidence.

### Recommended primary user

For the MVP, design primarily for an **AI product manager or AI engineering lead**. CFO and FinOps views can use the same data but do not require separate products.

### MVP economic boundary

Include:

- Model input-token cost
- Model output-token cost
- Tool-call cost
- Retry cost as a diagnostic subset of model/tool cost
- Fallback-model cost as a diagnostic subset of model cost
- Direct workflow compute cost when reliably measurable

Exclude initially:

- Employee salaries
- Shared corporate overhead
- Complex GPU allocation
- Full cloud invoices
- Revenue causality
- Enterprise chargeback

Retry and fallback values must not be added on top of model and tool totals when they refer to the same underlying calls.

### Core product promise

> OutcomeIQ shows how much successful AI work costs, where failed work wastes money and which workflow configuration produces the best economic result.

---

## 2. MVP User Journey

### Step 1 — Registration and login

The user creates an account or logs in.

The system establishes:

- User identity
- Organization membership
- Accessible projects

### Step 2 — Organization and project creation

The user creates:

- Organization: Acme Payments
- Project: AI Customer Support
- Default currency
- Project timezone

### Step 3 — Workflow registration

The user registers a workflow:

- Name: Payment Support Resolution
- Business owner
- Technical owner
- Description
- Workflow category
- Active configurations

The workflow is a business process, not an individual model call.

### Step 4 — Outcome Contract definition

The user defines:

- Unit of work: One customer-support ticket
- Success: Ticket resolved without human escalation
- Failure: Workflow cannot provide an accepted resolution
- Pending: Ticket awaiting customer, tool or human confirmation
- Abandoned: Workflow terminated without a final decision
- Reversed: Previously resolved ticket reopened within 48 hours
- Verification source: Ticketing system or authorised manual entry
- Finalisation window: 48 hours
- Quality requirement: No unsupported payment or refund claim

The contract is versioned so historical results retain their original success definition.

### Step 5 — Provider and model configuration

The user registers the models used by each configuration.

Example:

- Configuration A: Economy-first
- Configuration B: Quality-first
- Primary model
- Fallback model
- Input-token rate
- Output-token rate
- Effective date of the rate

No real AI-provider integration is required in the first version. Simulated call events and manually configured rate cards are sufficient.

### Step 6 — Workflow run starts

When a support ticket enters the workflow, OutcomeIQ creates a run with:

- Run identifier
- Workflow and configuration
- Synthetic or hashed ticket reference
- Start time
- Current status
- Outcome Contract version
- Correlation identifier

### Step 7 — Model calls are logged

For every model call, record:

- Model
- Sequence position
- Input tokens
- Output tokens
- Latency
- Status
- Calculated cost
- Parent workflow run

Prompt content should be omitted or represented only by an optional redacted hash.

### Step 8 — Tools, retries and fallbacks are logged

The workflow may call:

- Payment-status service
- Transaction-history service
- Refund-policy service

OutcomeIQ records whether each call:

- Succeeded
- Failed
- Timed out
- Was retried
- Triggered a fallback model

### Step 9 — Cost envelope is calculated

OutcomeIQ combines:

- Primary-model cost
- Fallback-model cost
- Tool cost
- Retry-call cost
- Direct compute cost

Each cost receives an attribution status:

- Exact
- Estimated
- Unattributed

### Step 10 — Final outcome is recorded

The ticket outcome becomes:

- Success
- Failure
- Pending
- Abandoned
- Reversed

Pending outcomes are excluded from finalised success yield until resolved, while their accumulated cost remains visible.

### Step 11 — Unit economics are calculated

The dashboard displays:

- Total attempts
- Finalised attempts
- Successful outcomes
- Pending outcomes
- Success yield
- Average cost per attempt
- Cost per successful outcome
- Failure waste
- Attribution coverage

### Step 12 — Failure waste is identified

OutcomeIQ highlights costs arising from:

- Failed model calls
- Failed tool calls
- Repeated calls
- Superseded responses
- Unproductive fallback paths
- Failed workflow runs

The product must distinguish confidently identified waste from suspected inefficiency.

### Step 13 — Configurations are compared

The user compares Economy-first and Quality-first configurations using:

- Similar ticket categories
- Same evaluation period
- Minimum sample threshold
- Cost per attempt
- Success yield
- Cost per successful outcome
- Failure-waste percentage
- Outcome latency
- Attribution coverage

### Step 14 — Recommendation is generated

OutcomeIQ assigns one decision:

- **Scale:** Best economics with acceptable quality and confidence
- **Keep:** Meets targets but has no strong reason to expand
- **Optimise:** Viable but contains identifiable waste
- **Investigate:** Evidence is insufficient, anomalous or contradictory
- **Restrict:** Suitable only for particular task segments
- **Stop:** Consistently fails economic or quality thresholds

The recommendation displays the metrics and rules responsible for the decision. Insufficient evidence must produce Investigate.

---

## 3. MVP Feature Prioritization

Database table names below are conceptual responsibilities. Detailed schema is defined separately in `database-design.md`.

## A. Must Have

| Feature | Purpose and user story | Backend requirement | Frontend requirement | Conceptual tables | Difficulty | Priority | Acceptance criteria |
|---|---|---|---|---|---|---|---|
| User authentication | As a user, I want secure registration and login so project data is protected. | Identity verification, password/session handling and JWT lifecycle | Registration, login, logout and error states | `users`, supporting auth sessions | Medium | High | User can register, log in and log out; protected data is inaccessible without authorization. |
| Organization and project setup | As a user, I want data separated by organization and project. | Tenant ownership, membership and project authorization | Organization/project creation and selector | `organizations`, `organization_members`, `projects`, `project_members` | Medium | High | User can create an organization/project and access only authorised projects. |
| Workflow registry | As an AI lead, I want to register each monitored business workflow. | Workflow metadata, versions, ownership and lifecycle status | Workflow list, creation and detail views | `workflows`, `workflow_versions` | Easy | High | User can create, update, activate and pause a support workflow. |
| Outcome Contract definition | As a product owner, I want an explicit definition of success. | Contract validation, versioning and state definitions | Guided contract form and readable summary | `outcome_contracts`, `outcome_contract_versions` | Hard | High | A workflow cannot activate without complete criteria; existing runs retain their contract version. |
| AI provider and model setup | As an engineer, I want to register simulated models and their rates. | Provider/model records and effective rate lookup | Provider, model and rate configuration | `ai_providers`, `ai_models`, `model_rate_cards` | Medium | High | User can register two providers and four models with effective input/output rates. |
| Workflow configuration management | As a product manager, I want Economy-first and Quality-first alternatives. | Configuration, model roles, retry and tool policies | Configuration creation and comparison-ready labels | `workflow_configurations`, `configuration_models` | Medium | High | At least two active configurations can belong to one workflow. |
| Workflow run tracking | As an engineer, I want one record for every ticket execution. | Run creation, lifecycle states, frozen references and timestamps | Run list and run-detail timeline | `workflow_runs`, `run_status_events` | Medium | High | Every demo ticket creates one identifiable run with immutable configuration and contract references. |
| Model-call logging | As an engineer, I want each model invocation connected to its run. | Idempotent call logging, ordering, model and parent-run association | Model-call timeline | `model_calls` | Medium | High | Every invocation appears under the correct run and configuration. |
| Token and latency tracking | As an engineer, I want usage and performance per model call. | Usage validation and aggregation | Per-call and per-run usage display | `model_calls` | Easy | High | Each model call records non-negative input/output tokens and latency. |
| Tool-call tracking | As an engineer, I want external tool cost and failure evidence. | Tool identity, status, latency, units and rate lookup | Tool-call timeline and status indicators | `tools`, `tool_calls`, `tool_rate_cards` | Medium | High | Successful, failed and timed-out calls are distinguishable and attached to a run. |
| Retry and fallback tracking | As an engineer, I want to see why additional calls occurred. | Parent-child attempt relationships and trigger reasons | Retry/fallback badges and sequence view | `run_attempts`, `model_calls`, `tool_calls` | Hard | High | A retry points to the failed attempt; a fallback identifies its trigger and replacement model. |
| Cost calculation and attribution | As a FinOps user, I want consistent cost for each execution component. | Rate lookup, deterministic calculation, deduplication and attribution | Itemised cost breakdown | `cost_entries`, `cost_attributions`, rate-card tables | Hard | High | Calls sum to run total without double counting; exact, estimated and unattributed values are separate. |
| Outcome event tracking | As a product owner, I want the business result independent from technical completion. | Append-only outcome transitions, verification and reversal | Outcome recording and history | `outcome_events`, `workflow_runs` | Hard | High | Success, failure, pending, abandoned and reversed are supported; reversal preserves history. |
| Attribution coverage and confidence | As a finance user, I want to know how complete the cost calculation is. | Coverage calculation and evidence classification | Coverage percentage and confidence labels | `cost_attributions`, `cost_entries` | Medium | High | Dashboard shows attributed, estimated and unattributed cost; demo coverage reaches at least 90%. |
| Cost per attempt | As a product manager, I want the average cost of initiating a workflow. | Known eligible cost divided by valid attempts | Metric card with definition | Derived from run and cost evidence | Easy | High | Metric matches controlled test data and excludes invalid demo runs. |
| Success yield | As a product manager, I want the percentage of finalised attempts that succeeded. | Verified current successes divided by finalised outcomes | Metric card and status breakdown | Derived from runs and outcomes | Easy | High | Pending outcomes are shown but excluded from the finalised denominator. |
| Cost per successful outcome | As a finance user, I want the unit cost of successful AI work. | Eligible known cost divided by verified successes | Metric card with numerator and denominator | Derived from costs and outcomes | Medium | High | Metric shows calculation period and returns not computable, not zero, when no success exists. |
| Failure-waste calculation | As an engineer, I want to locate money consumed without producing accepted value. | Evidence-backed, non-overlapping waste rules | Waste total, percentage and reason breakdown | `waste_events`, `cost_entries`, execution tables | Hard | High | Failed calls, retries and superseded responses are measurable and traceable to source cost. |
| Basic decision dashboard | As a user, I want one concise workflow-economics view. | Aggregated metric queries and filtering | Summary cards and four focused charts | Derived evidence; optional cached aggregates | Medium | High | Dashboard consistently shows required metrics for selected workflow and period. |
| Configuration comparison | As a product manager, I want to compare two configurations fairly. | Frozen cohorts, filters, sample counts and comparison calculations | Side-by-side comparison | `comparison_runs` | Hard | High | Same workflow, period and category can be compared with sample sizes visible. |
| Evidence-backed recommendation | As a decision-maker, I want an auditable recommendation. | Deterministic versioned rules, sufficiency checks and evidence links | Recommendation card and evidence panel | `recommendations`, `recommendation_evidence` | Hard | High | Every recommendation cites numerical evidence; insufficient evidence returns Investigate. |
| Audit history | As a reviewer, I want significant changes recorded. | Append-oriented audit service | Safe audit timeline | `audit_events` | Medium | High | Contract, rate, outcome, recalculation, membership and recommendation actions are auditable. |

## B. Should Have

| Feature | Purpose and user story | Backend requirement | Frontend requirement | Conceptual tables | Difficulty | Priority | Acceptance criteria |
|---|---|---|---|---|---|---|---|
| Model/tool rate versioning | As a FinOps user, I want historical runs calculated with rates active at execution time. | Effective-period resolution and immutable references | Rate history | Rate-card tables | Medium | Medium | Changing a current rate never silently alters historical cost. |
| Ticket-category segmentation | As a product manager, I want economics by ticket type. | Category filtering | Category filter and breakdown | `workflow_runs` | Medium | Medium | Payment, refund and account tickets can be compared independently. |
| Manual outcome verification | As an evaluator, I want to confirm demo outcomes. | Actor/source tracking and audit | Outcome verification form | `outcome_events`, `audit_events` | Easy | Medium | Manual outcomes identify who recorded them, when and from which source. |
| Basic cost anomaly detection | As an engineer, I want unusually expensive runs highlighted. | Simple statistical threshold or baseline | Anomaly badge and explanation | Derived analytics | Medium | Medium | A deliberately expensive demo run is detected without changing financial values. |
| Data export | As a researcher, I want evaluation data in a portable format. | Filtered export | Export action | Existing authoritative tables | Easy | Medium | User can export runs, costs, outcomes and configuration labels for a period. |
| Controlled demo-data mode | As a student, I want reproducible evaluation runs. | Deterministic seed and isolated reset | Demo scenario controls | Existing tables with demo marker | Medium | Medium | The same fixed seed reproduces the expected comparison. |

## C. Could Have

| Feature | Purpose and user story | Backend requirement | Frontend requirement | Conceptual tables | Difficulty | Priority | Acceptance criteria |
|---|---|---|---|---|---|---|---|
| Budget thresholds | Warn when cost per outcome exceeds a limit. | Threshold evaluation | Warning configuration | Future policy records | Medium | Low | Warning appears when the configured threshold is exceeded. |
| Simple outcome prediction | Estimate success probability for pending runs. | Basic calibrated model | Estimated probability clearly separated from verified outcome | Future prediction records | Hard | Low | Prediction never replaces authoritative outcome. |
| Human-review cost | Include escalation cost when reliable. | Fixed/manual review-cost rule | Separate review-cost breakdown | Future review evidence | Medium | Low | Review cost remains separate from model/tool cost. |
| Bounded AI explanation | Produce a concise evidence-grounded recommendation explanation. | Evidence-only context generation and validation | Explanation panel | Optional explanation record | Medium | Low | Every statement is supported by stored metrics; removing AI does not change the decision. |
| Basic economic forecast | Project monthly cost at expected volume. | Volume-based projection | Forecast assumptions and result | Future forecast record | Medium | Low | Forecast states volume, success-rate and unit-cost assumptions. |

## D. Future Version

| Feature | Purpose | Future requirement | Difficulty | Priority now |
|---|---|---|---|---|
| Cloud billing integration | Reconcile workflow economics with AWS, Azure and GCP invoices | Billing ingestion and reconciliation | Hard | Low |
| GPU cost allocation | Allocate shared GPU cost across inference workloads | Utilisation metering and allocation rules | Hard | Low |
| Enterprise chargeback | Assign spend to departments or customers | Accounting periods and allocation policies | Hard | Low |
| Autonomous model routing | Change model choice within approved constraints | Safe policy execution and rollback | Hard | Low |
| Full causal inference | Estimate causal contribution of workflow components | Experiments and causal modelling | Hard | Low |
| Additional verticals | Support legal, document, sales and code-review outcomes | Domain-specific Outcome Contracts | Hard | Low |
| Enterprise SSO and advanced RBAC | Corporate identity and granular permissions | Identity-provider integration | Hard | Low |
| Industry benchmarks | Compare economics using anonymous peer data | Privacy-preserving aggregation | Hard | Low |
| Large multi-agent optimisation | Specialist agents for controlled economic analysis | Agent orchestration and governance | Hard | Low |
| Mobile application | Mobile access to alerts and reports | Mobile authentication and interface | Medium | Low |

---

## 4. Feature-Level Design Principles

### 4.1 Financial calculations must be deterministic

LLMs may explain results but must not authoritatively calculate:

- Cost
- Success yield
- Cost per successful outcome
- Failure waste
- Attribution coverage

### 4.2 Outcome evidence is separate from workflow completion

A technically completed workflow is not automatically successful. Business outcome recording must remain an independent event.

### 4.3 Historical values must be reproducible

A historical run retains:

- Outcome Contract version
- Workflow version
- Workflow configuration
- Model and tool rates
- Outcome history
- Calculation version
- Recommendation evidence

### 4.4 Unknown values must remain unknown

The system must not silently treat:

- Pending as failure
- Unattributed cost as zero
- Missing tool cost as free
- Reopened tickets as permanent successes
- Low sample size as conclusive evidence

### 4.5 Recommendations must abstain when necessary

When evidence is insufficient, the correct recommendation is **Investigate**, not a fabricated optimisation.

---

## 5. MVP Boundaries

The MVP must not include the following.

### Infrastructure boundaries

- Full AWS, Azure or GCP invoice ingestion
- Multi-cloud cost reconciliation
- Kubernetes-wide cost allocation
- Universal GPU cost allocation
- Multi-region architecture
- Enterprise-scale data retention

### Financial boundaries

- Real payment processing
- Customer invoicing
- Tax or accounting functions
- Enterprise chargeback
- Financial-ledger replacement
- Complex revenue attribution
- Contract or procurement management

### AI boundaries

- Autonomous model switching
- Autonomous budget changes
- Full causal inference
- Custom foundation-model training
- Large multi-agent orchestration
- Natural-language FinOps chatbot
- AI-generated authoritative financial calculations

### Product boundaries

- More than one primary business vertical
- Many role-specific dashboards
- Mobile application
- Enterprise SSO
- Advanced permissions
- Public benchmark marketplace
- No-code workflow builder
- Replacement for existing LLM observability platforms

### Data boundaries

The MVP may store identifiers, metrics and redacted diagnostic evidence. It should not store complete customer conversations, payment information, card or bank data, secrets, access tokens or full prompts and responses.

---

## 6. Demo Scenario — AI Customer-Support Ticket Resolution

### Ticket

> “My payment failed but money was deducted.”

The operational database stores only a synthetic or hashed ticket reference and category, not the complete message.

### Outcome Contract

- **Unit:** One support ticket
- **Success:** Correct resolution supplied without human escalation and ticket remains closed for 48 hours
- **Pending:** Payment status remains unsettled
- **Failure:** Incorrect resolution or unresolved workflow
- **Abandoned:** Processing terminated without an outcome
- **Reversed:** Ticket reopened within 48 hours
- **Quality rule:** The AI cannot claim a refund was issued without tool confirmation

### Configuration A

**Economy-first**

- Economy model as primary
- Economy model permitted one retry
- Premium model used as fallback
- Maximum two payment-service attempts

### Example workflow run

| Sequence | Event | Usage/result | Latency | Cost |
|---:|---|---|---:|---:|
| 1 | Run started | Configuration A | — | — |
| 2 | Economy model call | 1,200 input, 180 output tokens | 1.1 s | $0.00174 |
| 3 | Payment-status tool | Timeout | 2.0 s | $0.00200 |
| 4 | Payment-status retry | Transaction found; pending settlement | 1.4 s | $0.00200 |
| 5 | Economy model follow-up | 900 input, 120 output tokens; fails quality rule | 0.9 s | $0.00126 |
| 6 | Premium fallback model | 1,400 input, 240 output tokens; compliant response | 1.8 s | $0.01060 |
| 7 | Refund-policy tool | Confirms expected reversal period | 0.7 s | $0.00200 |
| 8 | Run completed | Resolution sent | — | — |
| 9 | Outcome recorded | Success; not reopened after 48 hours | — | — |

### Run totals

- Total input tokens: 3,500
- Total output tokens: 540
- Model calls: 3
- Tool calls: 3
- Retry count: 1
- Fallback count: 1
- Total measured latency: 7.9 seconds
- Total attributable cost: **$0.01960**
- Final outcome: **Success**

### Failure-waste calculation

Clearly attributable waste:

- Timed-out payment tool: $0.00200
- Economy follow-up superseded after failing the quality rule: $0.00126

Total failure waste:

**$0.00326**

Failure-waste percentage:

**16.63% of the run cost**

The first model call is not classified as waste because it contributed to tool selection and workflow context.

### Attribution coverage

Assume total execution cost is estimated at $0.02060, including $0.00100 of unallocated shared compute.

- Directly attributed: $0.01960
- Unattributed: $0.00100
- Attribution coverage: **95.15%**

The system displays the unattributed portion rather than treating it as zero.

### Configuration comparison

Evaluate 100 comparable payment-support tickets per configuration.

| Metric | Configuration A: Economy-first | Configuration B: Quality-first |
|---|---:|---:|
| Attempts | 100 | 100 |
| Total cost | $1.20 | $1.60 |
| Average cost per attempt | **$0.01200** | $0.01600 |
| Successful outcomes | 55 | 82 |
| Finalised attempts | 92 | 95 |
| Finalised success yield | 59.78% | **86.32%** |
| Cost per successful outcome | $0.02182 | **$0.01951** |
| Failure-waste cost | $0.47 | $0.29 |
| Pending outcomes | 8 | 5 |

### Decision demonstrated

Configuration A appears cheaper using cost per attempt:

- A: $0.01200
- B: $0.01600

However, Configuration B is approximately **10.6% cheaper per successful outcome**, despite costing 33.3% more per attempt.

### Evidence-backed recommendation

**Recommendation for Configuration B: Scale**

Evidence:

- 86.32% finalised success yield versus 59.78%
- $0.01951 per successful outcome versus $0.02182
- Lower failure waste
- Same ticket category and evaluation period
- Sample size of 100 attempts per configuration

**Recommendation for Configuration A: Restrict and optimise**

Evidence:

- Lower request cost but higher successful-outcome cost
- Larger failed-workflow expenditure
- Frequent payment-tool retries
- Greater fallback dependence for complex payment tickets

This is the MVP’s central product demonstration.

---

## 7. MVP Success Criteria

## Functional completion

The MVP is complete when:

- Users can register and log in.
- A user can create an organization and project.
- A support workflow can be registered.
- An Outcome Contract can be defined and versioned.
- Two workflow configurations can be created.
- Model, tool, retry and fallback events can be recorded.
- Outcomes can transition between supported states.
- Required unit economics are calculated.
- Configuration comparison is available.
- Recommendations include supporting evidence.

## Required economic proof

- At least **90% of demo execution cost** is attributable to a workflow.
- Success, failure and pending outcomes are distinguishable.
- Abandoned and reversed outcomes are represented correctly.
- Retry and fallback waste is measurable.
- Two configurations can be compared.
- At least one experiment shows that the cheapest configuration per request is not the cheapest per successful outcome.
- Every recommendation links to numerical evidence.
- Insufficient evidence returns Investigate.
- Zero-success cases do not produce misleading zero metrics.

## Data-quality criteria

- No model or tool cost is counted twice.
- Historical cost uses the correct applicable rate.
- Pending outcomes are excluded from finalised success yield.
- Outcome reversals preserve historical evidence.
- Unattributed cost remains visible.
- Invalid or test runs can be excluded transparently.
- Recommendation cohorts and calculation versions are reproducible.

## Product-quality criteria

- The main demo can be completed without editing data manually behind the scenes.
- A user can understand the central comparison within two minutes.
- Recommendations are reproducible from their underlying rules.
- Failure waste can be traced to specific calls and cost entries.
- Sensitive prompt or customer content is unnecessary for the economic demonstration.

## Research-readiness criteria

The project should produce an exportable evaluation dataset containing:

- Workflow configuration
- Task category
- Model and tool usage
- Cost
- Retry/fallback behaviour
- Final outcome
- Quality status
- Recommendation

This allows the product demonstration to support a later research experiment.

---

## Recommended 12-Week Delivery Plan

| Weeks | Delivery focus |
|---|---|
| 1–2 | Finalise Outcome Contract semantics, demo workflow and evaluation dataset |
| 3 | Authentication, organization, project and workflow registry |
| 4 | Provider, model, rate and workflow configuration management |
| 5 | Workflow run, model-call and token tracking |
| 6 | Tool, retry and fallback tracking |
| 7 | Cost calculation, attribution and coverage |
| 8 | Outcome lifecycle and unit economics |
| 9 | Failure-waste classification and basic dashboard |
| 10 | Configuration comparison and recommendation rules |
| 11 | Live cloud integration, controlled experiments and anomaly cases |
| 12 | Testing, security review, documentation, deployment and final demonstration |

If schedule pressure occurs, remove Could Have features first. Do not weaken Outcome Contracts, cost correctness, outcome reconciliation or evidence traceability.

---

## 8. Final MVP Summary

The three-month OutcomeIQ MVP will prove that the economic value of an AI workflow cannot be judged from token cost or cost per request alone. Using a live customer-support workflow, it will connect model calls, tools, retries and fallbacks to verified ticket outcomes; calculate cost per successful resolution; expose failure waste; compare two configurations; and produce an auditable Scale, Keep, Optimise, Investigate, Restrict or Stop recommendation.

The completed MVP is successful when it demonstrates one defensible result:

> A workflow configuration that appears more expensive per request can be cheaper—and more valuable—per successful business outcome.
