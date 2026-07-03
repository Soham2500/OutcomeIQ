# OutcomeIQ — PostgreSQL Database Design

**Project:** OutcomeIQ — Outcome-aware AI FinOps Platform  
**Scope:** Three-month MVP  
**MVP vertical:** AI customer-support ticket resolution  
**Database:** PostgreSQL  
**Document status:** Logical database design; no tables or ORM models are created by this document

---

## 1. Database Design Overview

OutcomeIQ requires more than telemetry storage. Its database must preserve the evidence chain from an AI workflow execution to a verified business outcome and then to an economic recommendation.

The PostgreSQL design supports:

- **AI workflow tracking:** A workflow run records the selected workflow version, configuration, contract version and ticket category. Status events preserve its technical lifecycle.
- **Outcome Contracts:** Stable contract identities have immutable versions. Each run references the exact version used when it began.
- **Model and tool logging:** Model calls, tool calls, attempts, retries and fallbacks are attached to one workflow run and ordered for reconstruction.
- **Cost attribution:** Cost entries are generated from identifiable execution events and classified as exact, estimated or unattributed without hiding uncertainty.
- **Outcome reconciliation:** Append-only outcome events preserve pending, success, failure, abandoned and reversed states separately from technical run completion.
- **Unit economics:** Authoritative run costs and finalised outcomes support cost per attempt, success yield, cost per successful outcome and attribution coverage.
- **Failure-waste analysis:** Waste events reference the execution event and cost entry responsible for a measurable wasted amount.
- **Configuration comparison:** Comparison records preserve the two evaluated configurations, period, filters, sample sizes and metric snapshot.
- **Evidence-backed recommendations:** Recommendations preserve their rule version, calculation version, category, confidence and supporting evidence.
- **Auditability:** Audit events record important user and system actions using redacted summaries.

PostgreSQL is the sole authoritative store for these records. Redis may cache derived responses later, but cached data must be reproducible from PostgreSQL.

### Scope clarification

The requested entity list does not contain a `project_members` table, but project-level authorization cannot be represented correctly without it. This design therefore adds `project_members` as one small supporting table. All other entities follow the requested MVP scope.

---

## 2. Core Database Design Principles

### 2.1 Single source of truth

Execution, rate, cost, outcome, waste, recommendation and audit evidence is stored authoritatively in PostgreSQL. Derived dashboard values may be calculated on demand or cached, but the cache is never authoritative.

### 2.2 No double counting

Each economic charge is represented by one `cost_entries` row. Retry and fallback labels describe why a model or tool call occurred; they do not create a second copy of the underlying model or tool charge.

### 2.3 Historical reproducibility

Once referenced by a run, contract versions, workflow versions, configurations and rate-card records are immutable. Corrections create new versions or explicit adjustment records rather than silently modifying history.

### 2.4 Project-level data isolation

All project-owned operational entities carry or inherit a `project_id`. Backend queries must authorize the user through `project_members` before returning project data. Organization membership alone does not automatically imply access to every project.

### 2.5 Rate versioning

Model and tool rate cards contain effective periods. Calls reference the exact rate-card row used for their calculation. Historical rate cards are retired, not overwritten.

### 2.6 Outcome history preservation

`outcome_events` is append-only. A reversal adds a new event and retains the earlier success. The current outcome may be mirrored on `workflow_runs` for filtering, but the event history remains authoritative.

### 2.7 Explicit pending and unknown states

Pending outcomes are stored explicitly and excluded from finalised success yield. Missing amounts, unknown attribution and insufficient recommendation evidence are represented as unknown or insufficient rather than zero.

### 2.8 Sensitive-data minimisation

The database stores a synthetic or hashed ticket reference, ticket category and redacted evidence. It does not require complete conversations, payment information, bank data, secrets, access tokens or full prompts and responses.

### 2.9 Monetary precision

Monetary amounts use `NUMERIC(20,8)`. Token rates may be very small, so floating-point types must not be used for authoritative financial calculations. Currency uses a three-character `VARCHAR(3)` code.

### 2.10 Time consistency

All operational timestamps use `TIMESTAMPTZ` and are stored in UTC. Project timezone affects presentation only.

---

## 3. Entity Relationship Overview

```text
users
  │
  ├──< organization_members >── organizations
  │                                 │
  │                                 ├──< projects
  │                                 │      │
  └──< project_members >────────────┘      │
                                           ├──< workflows
                                           │      ├──< workflow_versions
                                           │      ├──< outcome_contracts
                                           │      │      └──< outcome_contract_versions
                                           │      └──< workflow_configurations
                                           │             └──< configuration_models >── ai_models
                                           │
                                           ├──< ai_providers
                                           │      └──< ai_models
                                           │             └──< model_rate_cards
                                           │
                                           ├──< tools
                                           │      └──< tool_rate_cards
                                           │
                                           └──< workflow_runs
                                                  ├── workflow_versions
                                                  ├── outcome_contract_versions
                                                  ├── workflow_configurations
                                                  ├──< run_status_events
                                                  ├──< run_attempts
                                                  ├──< model_calls ── model_rate_cards
                                                  ├──< tool_calls ─── tool_rate_cards
                                                  ├──< outcome_events
                                                  ├──< cost_entries
                                                  │      └──< cost_attributions
                                                  └──< waste_events ── cost_entries

workflows ──< comparison_runs >── workflow_configurations A/B
comparison_runs ──< recommendations ──< recommendation_evidence

users/projects/organizations ──< audit_events
```

### Relationship notes

- A workflow has many immutable workflow versions.
- A workflow has one active Outcome Contract at a time, while retaining retired contracts and all contract versions.
- A configuration belongs to one workflow and maps models to roles such as primary or fallback.
- A run references one workflow version, contract version and configuration.
- Calls and attempts belong to exactly one run.
- Cost and waste records are evidence derived from those execution records.
- A comparison evaluates two configurations of the same workflow.
- A recommendation belongs to one comparison and must have supporting evidence.

---

## 4. Table-by-Table Design

### Shared conventions

Unless stated otherwise:

- Primary keys use `UUID`.
- Mutable master records contain `created_at TIMESTAMPTZ` and `updated_at TIMESTAMPTZ`.
- Event records use `created_at` or a domain-specific event timestamp and are append-oriented.
- Foreign-key deletion is restricted for financial and historical evidence. Referenced records are archived rather than deleted.
- Examples are abbreviated logical records, not SQL statements.

### 4.1 `users`

- **Purpose:** Stores application identities.
- **Main columns:** `id UUID`, `email VARCHAR(320)`, `password_hash TEXT`, `display_name VARCHAR(120)`, `is_active BOOLEAN`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`, `last_login_at TIMESTAMPTZ NULL`.
- **Primary key:** `id`.
- **Foreign keys:** None.
- **Important indexes:** Unique functional index on lowercase email; index on `is_active`.
- **Important constraints:** Email required; password hash required; raw passwords prohibited.
- **Example record:** `email=architect@acme.demo`, `display_name=Demo Architect`, `is_active=true`.

### 4.2 `organizations`

- **Purpose:** Top-level tenant and ownership boundary.
- **Main columns:** `id UUID`, `name VARCHAR(160)`, `slug VARCHAR(100)`, `default_currency VARCHAR(3)`, `timezone VARCHAR(64)`, `created_by_user_id UUID`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `created_by_user_id → users.id`.
- **Important indexes:** Unique `slug`; index on `created_by_user_id`.
- **Important constraints:** Non-empty name; uppercase three-character currency.
- **Example record:** `name=Acme Payments`, `slug=acme-payments`, `default_currency=USD`, `timezone=Asia/Kolkata`.

### 4.3 `organization_members`

- **Purpose:** Connects users to organizations with an organization-level role.
- **Main columns:** `id UUID`, `organization_id UUID`, `user_id UUID`, `role user_role`, `is_active BOOLEAN`, `joined_at TIMESTAMPTZ`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `organization_id → organizations.id`; `user_id → users.id`.
- **Important indexes:** Unique composite `(organization_id, user_id)`; indexes on `user_id` and `(organization_id, role)`.
- **Important constraints:** One membership per user and organization.
- **Example record:** `organization=Acme Payments`, `user=Demo Architect`, `role=organization_owner`.

### 4.4 `projects`

- **Purpose:** Primary authorization and operational data boundary.
- **Main columns:** `id UUID`, `organization_id UUID`, `name VARCHAR(160)`, `slug VARCHAR(100)`, `description TEXT NULL`, `currency VARCHAR(3)`, `timezone VARCHAR(64)`, `is_active BOOLEAN`, `created_by_user_id UUID`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `organization_id → organizations.id`; `created_by_user_id → users.id`.
- **Important indexes:** Unique `(organization_id, slug)`; indexes on `organization_id` and `created_by_user_id`.
- **Important constraints:** Project currency fixed for MVP reporting; organization required.
- **Example record:** `name=AI Customer Support`, `slug=ai-customer-support`, `currency=USD`.

### 4.5 `project_members`

- **Purpose:** Enforces project-level access independently of organization membership.
- **Main columns:** `id UUID`, `project_id UUID`, `user_id UUID`, `role project_role`, `is_active BOOLEAN`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `project_id → projects.id`; `user_id → users.id`.
- **Important indexes:** Unique `(project_id, user_id)`; indexes on `user_id` and `(project_id, role)`.
- **Important constraints:** User must already be an active member of the project’s organization, enforced by the service transaction.
- **Example record:** `project=AI Customer Support`, `user=Demo Architect`, `role=project_owner`.

### 4.6 `workflows`

- **Purpose:** Stable identity for a monitored business workflow.
- **Main columns:** `id UUID`, `project_id UUID`, `name VARCHAR(180)`, `slug VARCHAR(120)`, `status workflow_status`, `business_owner_user_id UUID NULL`, `technical_owner_user_id UUID NULL`, `created_by_user_id UUID`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `project_id → projects.id`; owner and creator references → `users.id`.
- **Important indexes:** Unique `(project_id, slug)`; `(project_id, status)`; owner indexes.
- **Important constraints:** Archived workflows cannot accept new runs.
- **Example record:** `name=Payment Support Resolution`, `status=active`.

### 4.7 `workflow_versions`

- **Purpose:** Preserves the business and technical definition of a workflow at a point in time.
- **Main columns:** `id UUID`, `workflow_id UUID`, `version_number INTEGER`, `name VARCHAR(180)`, `description TEXT`, `vertical VARCHAR(80)`, `definition JSONB`, `change_summary TEXT NULL`, `created_by_user_id UUID`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_id → workflows.id`; `created_by_user_id → users.id`.
- **Important indexes:** Unique `(workflow_id, version_number)`; index on `workflow_id`.
- **Important constraints:** Version number positive; row immutable after a run references it.
- **Example record:** `version_number=1`, `vertical=customer_support`, `definition={ticket_categories:[payment,refund]}`.

### 4.8 `outcome_contracts`

- **Purpose:** Stable identity and lifecycle for a workflow’s definition of business success.
- **Main columns:** `id UUID`, `workflow_id UUID`, `name VARCHAR(180)`, `status contract_status`, `created_by_user_id UUID`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_id → workflows.id`; creator → `users.id`.
- **Important indexes:** `(workflow_id, status)`; partial unique index allowing one `active` contract per workflow.
- **Important constraints:** Only one active contract per workflow; active contract must have at least one version.
- **Example record:** `name=Verified Ticket Resolution Contract`, `status=active`.

### 4.9 `outcome_contract_versions`

- **Purpose:** Immutable success, failure, pending, abandonment and reversal rules used by runs.
- **Main columns:** `id UUID`, `outcome_contract_id UUID`, `version_number INTEGER`, `unit_of_work VARCHAR(120)`, `success_definition TEXT`, `failure_definition TEXT`, `pending_definition TEXT`, `abandoned_definition TEXT`, `reversal_definition TEXT`, `verification_source VARCHAR(120)`, `finalization_window_hours INTEGER`, `quality_rules JSONB`, `created_by_user_id UUID`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `outcome_contract_id → outcome_contracts.id`; creator → `users.id`.
- **Important indexes:** Unique `(outcome_contract_id, version_number)`; index on `outcome_contract_id`.
- **Important constraints:** Positive version; non-negative finalisation window; required definitions; immutable after reference.
- **Example record:** `unit_of_work=support_ticket`, `finalization_window_hours=48`, `verification_source=ticketing_system`, `quality_rules={refund_claim_requires_tool_confirmation:true}`.

### 4.10 `ai_providers`

- **Purpose:** Registry of simulated and future AI model providers.
- **Main columns:** `id UUID`, `organization_id UUID`, `name VARCHAR(120)`, `provider_key VARCHAR(80)`, `is_simulated BOOLEAN`, `is_active BOOLEAN`, `metadata JSONB`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `organization_id → organizations.id`.
- **Important indexes:** Unique `(organization_id, provider_key)`; indexes on `organization_id` and `is_active`.
- **Important constraints:** Secrets are not stored in `metadata`; provider key non-empty.
- **Example record:** `name=SimuLean AI`, `provider_key=simulean`, `is_simulated=true`.

### 4.11 `ai_models`

- **Purpose:** Registry of models offered by a provider.
- **Main columns:** `id UUID`, `provider_id UUID`, `model_key VARCHAR(120)`, `display_name VARCHAR(160)`, `model_family VARCHAR(100) NULL`, `is_active BOOLEAN`, `capabilities JSONB`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `provider_id → ai_providers.id`.
- **Important indexes:** Unique `(provider_id, model_key)`; indexes on `provider_id` and `(provider_id, is_active)`.
- **Important constraints:** A model cannot change provider after creation.
- **Example record:** `model_key=economy-s`, `display_name=Economy S`, `capabilities={support:true}`.

### 4.12 `model_rate_cards`

- **Purpose:** Versioned token-pricing evidence for a model.
- **Main columns:** `id UUID`, `model_id UUID`, `currency VARCHAR(3)`, `input_price_per_million NUMERIC(20,8)`, `output_price_per_million NUMERIC(20,8)`, `fixed_call_price NUMERIC(20,8)`, `effective_from TIMESTAMPTZ`, `effective_to TIMESTAMPTZ NULL`, `source VARCHAR(120)`, `is_estimated BOOLEAN`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `model_id → ai_models.id`.
- **Important indexes:** `(model_id, effective_from DESC)`; unique `(model_id, currency, effective_from)`; index on effective range.
- **Important constraints:** Prices non-negative; `effective_to > effective_from`; service prevents overlapping active periods for the same model and currency; row immutable once referenced.
- **Example record:** `model=Economy S`, `input_price_per_million=1.00000000`, `output_price_per_million=3.00000000`, `effective_from=2026-07-01T00:00:00Z`.

### 4.13 `tools`

- **Purpose:** Registry of external tools invoked by support workflows.
- **Main columns:** `id UUID`, `project_id UUID`, `tool_key VARCHAR(100)`, `display_name VARCHAR(160)`, `description TEXT NULL`, `is_active BOOLEAN`, `metadata JSONB`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `project_id → projects.id`.
- **Important indexes:** Unique `(project_id, tool_key)`; `(project_id, is_active)`.
- **Important constraints:** Metadata contains no credentials or customer data.
- **Example record:** `tool_key=payment_status`, `display_name=Payment Status Lookup`.

### 4.14 `tool_rate_cards`

- **Purpose:** Versioned unit pricing for tool invocations.
- **Main columns:** `id UUID`, `tool_id UUID`, `currency VARCHAR(3)`, `unit_name VARCHAR(40)`, `unit_price NUMERIC(20,8)`, `effective_from TIMESTAMPTZ`, `effective_to TIMESTAMPTZ NULL`, `source VARCHAR(120)`, `is_estimated BOOLEAN`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `tool_id → tools.id`.
- **Important indexes:** `(tool_id, effective_from DESC)`; unique `(tool_id, currency, effective_from)`.
- **Important constraints:** Unit price non-negative; valid effective interval; no overlapping effective periods per tool/currency/unit, enforced by service.
- **Example record:** `tool=Payment Status Lookup`, `unit_name=call`, `unit_price=0.00200000`.

### 4.15 `workflow_configurations`

- **Purpose:** Defines an immutable executable alternative such as Economy-first or Quality-first.
- **Main columns:** `id UUID`, `workflow_id UUID`, `workflow_version_id UUID`, `name VARCHAR(160)`, `configuration_key VARCHAR(100)`, `status configuration_status`, `settings JSONB`, `created_by_user_id UUID`, timestamps.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_id → workflows.id`; `workflow_version_id → workflow_versions.id`; creator → `users.id`.
- **Important indexes:** Unique `(workflow_id, configuration_key)`; `(workflow_id, status)`.
- **Important constraints:** Workflow version must belong to the same workflow; configurations become immutable after first use and are replaced by a new configuration record when materially changed.
- **Example record:** `name=Economy-first`, `configuration_key=economy-first-v1`, `status=active`, `settings={max_tool_retries:1}`.

### 4.16 `configuration_models`

- **Purpose:** Maps models to roles inside a workflow configuration.
- **Main columns:** `id UUID`, `configuration_id UUID`, `model_id UUID`, `model_role VARCHAR(32)`, `priority INTEGER`, `max_calls INTEGER NULL`, `conditions JSONB`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `configuration_id → workflow_configurations.id`; `model_id → ai_models.id`.
- **Important indexes:** Unique `(configuration_id, model_role, priority)`; indexes on `configuration_id` and `model_id`.
- **Important constraints:** Priority positive; role limited to `primary`, `fallback`, `specialist` for MVP; at least one primary model per active configuration.
- **Example record:** `configuration=Economy-first`, `model=Economy S`, `model_role=primary`, `priority=1`.

### 4.17 `workflow_runs`

- **Purpose:** Central record for one support-ticket execution.
- **Main columns:** `id UUID`, `project_id UUID`, `workflow_id UUID`, `workflow_version_id UUID`, `configuration_id UUID`, `outcome_contract_version_id UUID`, `external_ticket_ref_hash VARCHAR(128)`, `ticket_category VARCHAR(80)`, `run_status run_status`, `technical_status technical_status`, `current_outcome_status outcome_status`, `started_at TIMESTAMPTZ`, `completed_at TIMESTAMPTZ NULL`, `outcome_finalized_at TIMESTAMPTZ NULL`, `correlation_id UUID`, `metadata JSONB`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** Project, workflow, workflow version, configuration and contract-version references to their respective tables.
- **Important indexes:** `(project_id, created_at DESC)`, `(workflow_id, created_at DESC)`, `(configuration_id, created_at DESC)`, `(project_id, ticket_category, created_at)`, `(project_id, current_outcome_status, created_at)`, unique `correlation_id`.
- **Important constraints:** All referenced entities must belong to the same project/workflow; completion cannot precede start; external reference is synthetic or hashed; current outcome is a transactional projection of the latest outcome event.
- **Example record:** `ticket_category=payment_failure`, `run_status=completed`, `technical_status=succeeded`, `current_outcome_status=success`.

### 4.18 `run_status_events`

- **Purpose:** Append-only technical lifecycle history for a workflow run.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `run_status run_status`, `technical_status technical_status`, `reason_code VARCHAR(80) NULL`, `reason_text TEXT NULL`, `occurred_at TIMESTAMPTZ`, `recorded_by_user_id UUID NULL`, `metadata JSONB`.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_run_id → workflow_runs.id`; actor → `users.id`.
- **Important indexes:** `(workflow_run_id, occurred_at)`; `(run_status, occurred_at)`.
- **Important constraints:** Append-only; event order must follow valid run-state transitions.
- **Example record:** `run_status=running`, `technical_status=in_progress`, `reason_code=workflow_started`.

### 4.19 `run_attempts`

- **Purpose:** Groups retries and fallback execution phases without duplicating call cost.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `parent_attempt_id UUID NULL`, `attempt_number INTEGER`, `attempt_type VARCHAR(32)`, `trigger_reason VARCHAR(120) NULL`, `technical_status technical_status`, `started_at TIMESTAMPTZ`, `ended_at TIMESTAMPTZ NULL`, `metadata JSONB`.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_run_id → workflow_runs.id`; `parent_attempt_id → run_attempts.id`.
- **Important indexes:** Unique `(workflow_run_id, attempt_number)`; `(workflow_run_id, parent_attempt_id)`.
- **Important constraints:** Positive attempt number; attempt type limited to `initial`, `retry`, `fallback`; parent attempt must belong to the same run; end cannot precede start.
- **Example record:** `attempt_number=2`, `attempt_type=retry`, `trigger_reason=payment_tool_timeout`.

### 4.20 `model_calls`

- **Purpose:** Records one simulated or future real model invocation.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `run_attempt_id UUID`, `model_id UUID`, `model_rate_card_id UUID NULL`, `parent_model_call_id UUID NULL`, `sequence_number INTEGER`, `call_role VARCHAR(32)`, `status call_status`, `input_tokens INTEGER`, `output_tokens INTEGER`, `latency_ms INTEGER`, `started_at TIMESTAMPTZ`, `completed_at TIMESTAMPTZ NULL`, `error_code VARCHAR(80) NULL`, `redacted_evidence JSONB`, `idempotency_key VARCHAR(160)`.
- **Primary key:** `id`.
- **Foreign keys:** Run, attempt, model, rate card and parent-call references.
- **Important indexes:** `(workflow_run_id, sequence_number)`, `(model_id, started_at)`, `(model_rate_card_id)`, `(status, started_at)`, unique `(workflow_run_id, idempotency_key)`.
- **Important constraints:** Tokens and latency non-negative; model rate card, when present, must belong to the model and be effective at call time; parent call belongs to the same run; prompts and responses are not stored by default.
- **Example record:** `call_role=primary`, `status=succeeded`, `input_tokens=1200`, `output_tokens=180`, `latency_ms=1100`.

### 4.21 `tool_calls`

- **Purpose:** Records one external tool invocation, including retries.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `run_attempt_id UUID`, `tool_id UUID`, `tool_rate_card_id UUID NULL`, `parent_tool_call_id UUID NULL`, `sequence_number INTEGER`, `status tool_call_status`, `units NUMERIC(20,8)`, `latency_ms INTEGER`, `started_at TIMESTAMPTZ`, `completed_at TIMESTAMPTZ NULL`, `error_code VARCHAR(80) NULL`, `redacted_evidence JSONB`, `idempotency_key VARCHAR(160)`.
- **Primary key:** `id`.
- **Foreign keys:** Run, attempt, tool, rate card and parent-call references.
- **Important indexes:** `(workflow_run_id, sequence_number)`, `(tool_id, started_at)`, `(tool_rate_card_id)`, `(status, started_at)`, unique `(workflow_run_id, idempotency_key)`.
- **Important constraints:** Units and latency non-negative; rate card must belong to the tool and be effective at call time; retry parent belongs to the same run.
- **Example record:** `tool=Payment Status Lookup`, `status=timed_out`, `units=1`, `latency_ms=2000`.

### 4.22 `outcome_events`

- **Purpose:** Append-only business-outcome history independent of technical status.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `previous_status outcome_status NULL`, `outcome_status outcome_status`, `is_verified BOOLEAN`, `verification_source VARCHAR(120)`, `source_reference_hash VARCHAR(128) NULL`, `recorded_by_user_id UUID NULL`, `reason TEXT`, `evidence JSONB`, `occurred_at TIMESTAMPTZ`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `workflow_run_id → workflow_runs.id`; recorder → `users.id`.
- **Important indexes:** `(workflow_run_id, occurred_at)`, `(outcome_status, occurred_at)`, `(recorded_by_user_id, occurred_at)`.
- **Important constraints:** Append-only; valid transition required; manual verification requires actor; success/failure/reversal requires a verification source; evidence redacted.
- **Example record:** `previous_status=pending`, `outcome_status=success`, `is_verified=true`, `verification_source=ticketing_system`, `reason=ticket remained closed for 48 hours`.

### 4.23 `cost_entries`

- **Purpose:** Authoritative ledger-like record of each direct workflow charge.
- **Main columns:** `id UUID`, `project_id UUID`, `workflow_run_id UUID`, `cost_type cost_type`, `source_model_call_id UUID NULL`, `source_tool_call_id UUID NULL`, `source_run_attempt_id UUID NULL`, `amount NUMERIC(20,8) NULL`, `currency VARCHAR(3)`, `quantity NUMERIC(20,8) NULL`, `unit VARCHAR(40) NULL`, `unit_rate NUMERIC(20,8) NULL`, `model_rate_card_id UUID NULL`, `tool_rate_card_id UUID NULL`, `calculation_version VARCHAR(40)`, `included_in_run_total BOOLEAN`, `deduplication_key VARCHAR(180)`, `calculated_at TIMESTAMPTZ`, `metadata JSONB`.
- **Primary key:** `id`.
- **Foreign keys:** Project, run, source-event and rate-card references.
- **Important indexes:** `(workflow_run_id, calculated_at)`, `(project_id, calculated_at)`, source-event indexes, unique `(project_id, deduplication_key)`.
- **Important constraints:** Amount, quantity and unit rate non-negative when present; at most one direct source event; exact/estimated event cost should have exactly one source; source event must belong to the same run; one included inference cost per model call and one included usage cost per tool call; unknown amount remains `NULL`, not zero.
- **Example record:** `cost_type=model_inference`, `amount=0.00174000`, `quantity=1380`, `unit=tokens`, `calculation_version=cost-v1`, `included_in_run_total=true`.

### 4.24 `cost_attributions`

- **Purpose:** States how confidently a cost entry is attributable to a workflow run and why.
- **Main columns:** `id UUID`, `cost_entry_id UUID`, `workflow_run_id UUID`, `attribution_type attribution_type`, `attributed_amount NUMERIC(20,8) NULL`, `confidence_level confidence_level`, `method VARCHAR(80)`, `reason TEXT NULL`, `evidence JSONB`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** `cost_entry_id → cost_entries.id`; `workflow_run_id → workflow_runs.id`.
- **Important indexes:** Unique `cost_entry_id` for the MVP’s single primary attribution; `(workflow_run_id, attribution_type)`.
- **Important constraints:** Attributed amount non-negative; run matches the cost entry; exact attribution requires known amount and direct evidence; unknown amount may remain null for unattributed entries.
- **Example record:** `attribution_type=exact`, `attributed_amount=0.00174000`, `confidence_level=high`, `method=token_rate_card`.

### 4.25 `waste_events`

- **Purpose:** Evidence-backed classification of a cost amount that did not contribute to the accepted outcome.
- **Main columns:** `id UUID`, `workflow_run_id UUID`, `waste_type waste_type`, `source_model_call_id UUID NULL`, `source_tool_call_id UUID NULL`, `source_run_attempt_id UUID NULL`, `cost_entry_id UUID`, `waste_amount NUMERIC(20,8)`, `currency VARCHAR(3)`, `confidence_level confidence_level`, `classification_version VARCHAR(40)`, `reason TEXT`, `evidence JSONB`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** Run, source execution event and cost entry references.
- **Important indexes:** `(workflow_run_id, created_at)`, `(waste_type, created_at)`, `cost_entry_id`, source-event indexes.
- **Important constraints:** Exactly one source execution event; waste amount non-negative and cannot exceed the referenced cost entry amount, enforced transactionally; all references belong to the same run; duplicate waste classification for the same cost portion prohibited.
- **Example record:** `waste_type=failed_tool_call`, `waste_amount=0.00200000`, `confidence_level=high`, `reason=payment lookup timed out and was retried`.

### 4.26 `comparison_runs`

- **Purpose:** Reproducible comparison execution between two workflow configurations.
- **Main columns:** `id UUID`, `project_id UUID`, `workflow_id UUID`, `configuration_a_id UUID`, `configuration_b_id UUID`, `period_start TIMESTAMPTZ`, `period_end TIMESTAMPTZ`, `ticket_category VARCHAR(80) NULL`, `filters JSONB`, `cohort_a_run_ids JSONB`, `cohort_b_run_ids JSONB`, `sample_size_a INTEGER`, `sample_size_b INTEGER`, `metrics_a JSONB`, `metrics_b JSONB`, `calculation_version VARCHAR(40)`, `comparison_status VARCHAR(24)`, `insufficiency_reason TEXT NULL`, `created_by_user_id UUID`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** Project, workflow, both configurations and creator references.
- **Important indexes:** `(workflow_id, created_at DESC)`, configuration indexes, `(project_id, period_start, period_end)`.
- **Important constraints:** Configurations must differ and belong to the same workflow; period end after start; sample sizes non-negative; status limited to `completed`, `insufficient`, `failed`; cohort identifiers contain only runs from the corresponding configuration. JSONB cohort storage is acceptable at MVP scale; a normalized membership table is a future optimization.
- **Example record:** `configuration_a=Economy-first`, `configuration_b=Quality-first`, `sample_size_a=100`, `sample_size_b=100`, `comparison_status=completed`.

### 4.27 `recommendations`

- **Purpose:** Stores an auditable decision generated from one comparison.
- **Main columns:** `id UUID`, `project_id UUID`, `workflow_id UUID`, `comparison_run_id UUID`, `recommendation_category recommendation_category`, `target_configuration_id UUID NULL`, `confidence_level confidence_level`, `rule_version VARCHAR(40)`, `calculation_version VARCHAR(40)`, `period_start TIMESTAMPTZ`, `period_end TIMESTAMPTZ`, `sample_size INTEGER`, `reason TEXT`, `is_current BOOLEAN`, `generated_at TIMESTAMPTZ`, `generated_by_user_id UUID NULL`.
- **Primary key:** `id`.
- **Foreign keys:** Project, workflow, comparison, optional target configuration and optional user references.
- **Important indexes:** `(workflow_id, generated_at DESC)`, `(project_id, recommendation_category, generated_at)`, `(target_configuration_id, generated_at)`, partial index on current recommendations.
- **Important constraints:** Category `investigate` required when comparison is insufficient or confidence is insufficient; period and sample must match comparison snapshot; recommendation and evidence rows created in one transaction; old recommendations retained and marked non-current.
- **Example record:** `recommendation_category=scale`, `target_configuration=Quality-first`, `confidence_level=high`, `rule_version=recommendation-v1`.

### 4.28 `recommendation_evidence`

- **Purpose:** Stores numerical and linked evidence supporting a recommendation.
- **Main columns:** `id UUID`, `recommendation_id UUID`, `evidence_key VARCHAR(100)`, `metric_name VARCHAR(120)`, `metric_value NUMERIC(20,8) NULL`, `metric_unit VARCHAR(40) NULL`, `comparison_operator VARCHAR(16) NULL`, `threshold_value NUMERIC(20,8) NULL`, `configuration_id UUID NULL`, `comparison_run_id UUID NULL`, `cost_entry_id UUID NULL`, `waste_event_id UUID NULL`, `outcome_event_id UUID NULL`, `evidence JSONB`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** Recommendation and optional configuration/comparison/cost/waste/outcome references.
- **Important indexes:** `(recommendation_id, evidence_key)`, referenced-entity indexes.
- **Important constraints:** Unique `(recommendation_id, evidence_key)`; at least one metric or entity link required; linked records must belong to the same project/workflow context; every recommendation requires evidence before transaction commit.
- **Example record:** `evidence_key=cpso_quality_first`, `metric_name=cost_per_successful_outcome`, `metric_value=0.01951000`, `metric_unit=USD/outcome`.

### 4.29 `audit_events`

- **Purpose:** Append-oriented record of significant user and system actions.
- **Main columns:** `id UUID`, `organization_id UUID NULL`, `project_id UUID NULL`, `actor_user_id UUID NULL`, `action_type audit_action_type`, `entity_type VARCHAR(80)`, `entity_id UUID NULL`, `request_correlation_id UUID NULL`, `before_summary JSONB NULL`, `after_summary JSONB NULL`, `reason TEXT NULL`, `ip_hash VARCHAR(128) NULL`, `created_at TIMESTAMPTZ`.
- **Primary key:** `id`.
- **Foreign keys:** Organization, project and actor references.
- **Important indexes:** `(project_id, created_at DESC)`, `(organization_id, created_at DESC)`, `(actor_user_id, action_type, created_at DESC)`, `(entity_type, entity_id)`.
- **Important constraints:** Append-only; either actor or explicit system action context required; summaries must be redacted; secrets and full customer content prohibited.
- **Example record:** `action_type=verify_outcome`, `entity_type=workflow_run`, `actor_user=Demo Architect`, `reason=48-hour closure verified`.

---

## 5. Required ENUMs

PostgreSQL ENUMs are appropriate for stable domain states. Values should be lowercase and application-facing labels may be formatted separately.

| ENUM | Values | Meaning |
|---|---|---|
| `user_role` | `organization_owner`, `organization_admin`, `member` | Organization-level authority |
| `project_role` | `project_owner`, `editor`, `analyst`, `viewer` | Project-level authorization |
| `workflow_status` | `draft`, `active`, `paused`, `archived` | Workflow lifecycle |
| `contract_status` | `draft`, `active`, `retired` | Outcome Contract lifecycle |
| `configuration_status` | `draft`, `active`, `paused`, `archived` | Configuration lifecycle |
| `run_status` | `created`, `running`, `completed`, `cancelled` | Overall execution lifecycle |
| `technical_status` | `not_started`, `in_progress`, `succeeded`, `failed`, `timed_out` | Technical execution result |
| `outcome_status` | `pending`, `success`, `failure`, `abandoned`, `reversed` | Verified business outcome state |
| `call_status` | `queued`, `running`, `succeeded`, `failed`, `timed_out`, `cancelled`, `rejected`, `superseded` | Model-call state |
| `tool_call_status` | `queued`, `running`, `succeeded`, `failed`, `timed_out`, `cancelled` | Tool-call state |
| `cost_type` | `model_inference`, `tool_usage`, `external_api`, `direct_compute`, `unknown` | Economic source; retry/fallback never duplicate the underlying type |
| `attribution_type` | `exact`, `estimated`, `unattributed` | Confidence class for assignment to the run |
| `waste_type` | `failed_model_call`, `failed_tool_call`, `retry_caused_by_failure`, `superseded_response`, `unproductive_fallback`, `failed_workflow_run` | Evidence-backed waste classification |
| `recommendation_category` | `scale`, `keep`, `optimise`, `investigate`, `restrict`, `stop` | Product decision outcome |
| `confidence_level` | `insufficient`, `low`, `medium`, `high` | Evidence confidence or sufficiency |
| `audit_action_type` | `login`, `logout`, `create`, `update`, `activate`, `pause`, `archive`, `add_member`, `remove_member`, `verify_outcome`, `reverse_outcome`, `calculate_cost`, `classify_waste`, `run_comparison`, `generate_recommendation`, `export` | Audited action category |

### ENUM design note

`retry` and `fallback` are intentionally not `cost_type` values. Their model or tool consumption already has a cost entry. Attempts and waste events describe the retry/fallback context without creating duplicate costs.

---

## 6. Historical Reproducibility Design

### Contract version used by each run

`workflow_runs.outcome_contract_version_id` points directly to the immutable contract version active when the run began. Activating a later contract version does not alter earlier runs.

### Workflow version and configuration

Every run references `workflow_version_id` and `configuration_id`. A configuration is frozen after first use. Material changes create a new configuration instead of editing an executed configuration.

### Model rate used by each model call

`model_calls.model_rate_card_id` identifies the applicable rate. `cost_entries` additionally stores the quantity, unit rate, amount and calculation version used. Rate cards are immutable once referenced.

### Tool rate used by each tool call

`tool_calls.tool_rate_card_id` and the corresponding cost entry preserve the rate and quantity applied to the call, including retry calls.

### Outcome state history

`outcome_events` never overwrites earlier states. The latest valid event defines the current outcome. `workflow_runs.current_outcome_status` is a query optimization updated in the same transaction.

### Recommendation rule version

Each recommendation stores `rule_version`. A later rule release generates a new recommendation rather than rewriting the old one.

### Calculation version

Cost entries, waste events, comparisons and recommendations store calculation or classification versions. This makes results reproducible even if formulas improve later.

### Recalculation policy

A recalculation produces new versioned derived records or a clearly audited replacement. Authoritative raw calls, original rates and outcome events remain unchanged.

---

## 7. Cost Attribution Design

### 7.1 Role of `cost_entries`

`cost_entries` is the authoritative source for run totals. Each row represents one real economic charge or one explicitly unknown charge.

Examples:

- One model call → one model-inference cost entry.
- One payment-tool call → one tool-usage cost entry.
- A retry tool call → its own tool-usage entry because it is a separate billed invocation.
- A fallback model call → its own inference entry because it is a separate invocation.
- Missing shared compute amount → an `unknown` entry with a null amount and an explanation.

The retry or fallback does not receive an additional duplicate “retry fee” unless an external provider actually charges such a fee.

### 7.2 Role of `cost_attributions`

`cost_attributions` describes the strength and method of attribution:

- **Exact:** Usage and applicable rate are known.
- **Estimated:** Amount is computed using an approved estimate or manually configured rate.
- **Unattributed:** The charge is known to exist but its precise source or amount cannot be established.

For the MVP, each cost entry has one primary attribution. Future allocation across multiple runs can relax this rule.

### 7.3 Source-event rule

Where possible, a cost entry references exactly one of:

- `source_model_call_id`
- `source_tool_call_id`
- `source_run_attempt_id`

Unattributed shared cost may have no source execution event, but it must retain a reason and remain visible.

### 7.4 Preventing double counting

- A unique deduplication key protects repeated ingestion.
- A model call can have only one included inference cost entry.
- A tool call can have only one included tool-usage cost entry.
- Waste events reference cost entries; they do not add to the run total.
- Comparison and recommendation records store metric snapshots but never become financial ledger entries.

### 7.5 Reproducible run total

The authoritative known run total is the sum of `amount` for that run where `included_in_run_total=true`. Unknown-amount entries are reported separately and do not silently become zero.

Attribution coverage is calculated from known, attributed cost relative to the known or estimated total cost envelope. The dashboard must show its numerator, denominator and unknown count.

---

## 8. Outcome Reconciliation Design

Technical completion and business success are independent dimensions:

- A workflow may technically succeed while the ticket remains pending.
- A workflow may technically succeed but produce a business failure.
- A successful ticket may later be reversed.

### Outcome-state handling

- **Pending:** Initial unresolved business state. Excluded from finalised success yield.
- **Success:** Verified completion under the referenced Outcome Contract.
- **Failure:** Verified failure to meet the contract.
- **Abandoned:** Processing ended without a valid resolution; treated as a finalised non-success.
- **Reversed:** A previously successful result was invalidated, such as a ticket reopening within 48 hours.

### Valid MVP transitions

```text
no outcome → pending
pending → success
pending → failure
pending → abandoned
success → reversed
```

Administrative correction should append a new audited event; it must never delete prior history. Complex correction workflows are outside the MVP.

### Finalised success yield

Pending runs are excluded from the denominator. Finalised states are success, failure, abandoned and reversed. A reversed run is not counted as a current success, although its earlier success event remains visible.

### Manual verification

Manual outcome events require:

- `recorded_by_user_id`
- Verification source
- Reason
- Redacted evidence
- Audit event

System-recorded events may use a null actor but must identify a system source in evidence.

---

## 9. Failure-Waste Design

`waste_events` classifies measurable wasted cost without changing the underlying run total.

| Waste type | Meaning | Typical evidence |
|---|---|---|
| `failed_model_call` | Billed model invocation failed technically | Failed call status and associated inference cost |
| `failed_tool_call` | Tool invocation failed or timed out | Tool status, error code and tool cost |
| `retry_caused_by_failure` | Additional billed attempt was required by a prior failure | Parent attempt/call relationship and retry cost |
| `superseded_response` | Completed response was rejected and replaced | Rejected/superseded status and fallback relationship |
| `unproductive_fallback` | Fallback increased cost without improving accepted outcome | Fallback call plus failed/unchanged outcome evidence |
| `failed_workflow_run` | Costs from a finalised failed or abandoned run | Run total and final outcome evidence |

Every waste event must link to:

- One workflow run
- One source execution event
- One cost entry
- One waste type
- A reason
- Redacted evidence
- A classification version
- A confidence level

### Partial waste

`waste_amount` may equal all or part of the referenced cost entry. The total waste allocated against a cost entry must not exceed its known amount. This aggregate validation is enforced in the service transaction because it spans multiple rows.

### Avoiding inflated waste

The same cost portion cannot be classified twice. In particular, a failed workflow run should not blindly duplicate all cost already classified as failed calls. Reporting may show overlapping diagnostic categories only if it clearly uses non-additive views; the authoritative failure-waste total must use mutually exclusive allocated amounts.

---

## 10. Recommendation Evidence Design

### Recommendation record

`recommendations` stores:

- Category: Scale, Keep, Optimise, Investigate, Restrict or Stop
- Target configuration where applicable
- Rule version
- Calculation version
- Comparison period
- Sample size
- Confidence level
- Human-readable reason
- Current/historical status

### Evidence records

`recommendation_evidence` stores one row per relevant metric or source, such as:

- Cost per attempt for each configuration
- Cost per successful outcome for each configuration
- Success yield
- Failure-waste amount and percentage
- Attribution coverage
- Pending count
- Sample-size threshold
- Comparison run
- Relevant waste or outcome evidence

### Evidence sufficiency rule

If any mandatory condition fails—such as insufficient sample size, low attribution coverage, excessive pending outcomes or incomparable cohorts—the category must be `investigate` with `confidence_level=insufficient` or `low`.

### Transactional completeness

The recommendation and its evidence rows are created in one database transaction. A recommendation is not exposed as current until at least the mandatory evidence set exists.

### Immutability

Generated recommendations are historical evidence. Re-evaluation creates a new recommendation and marks the previous one non-current.

---

## 11. Indexing Strategy

Indexes should support tenant isolation, run reconstruction and time-bound analytics without attempting enterprise-scale optimization prematurely.

### Tenant and authorization indexes

- `organization_members (organization_id, user_id)` unique
- `project_members (project_id, user_id)` unique
- `projects (organization_id, slug)` unique
- Project-owned tables indexed by `project_id`

### Workflow and configuration indexes

- `workflows (project_id, status)`
- `workflow_versions (workflow_id, version_number)` unique
- `workflow_configurations (workflow_id, status)`
- `configuration_models (configuration_id, model_role, priority)`

### Run and event indexes

- `workflow_runs (project_id, created_at DESC)`
- `workflow_runs (workflow_id, created_at DESC)`
- `workflow_runs (configuration_id, created_at DESC)`
- `workflow_runs (project_id, ticket_category, created_at)`
- `workflow_runs (project_id, current_outcome_status, created_at)`
- `run_status_events (workflow_run_id, occurred_at)`
- `outcome_events (workflow_run_id, occurred_at)`

### Provider, model and rate indexes

- `ai_providers (organization_id, provider_key)` unique
- `ai_models (provider_id, model_key)` unique
- `model_rate_cards (model_id, effective_from DESC)`
- `tool_rate_cards (tool_id, effective_from DESC)`
- `model_calls (model_id, started_at)`

### Cost and waste indexes

- `cost_entries (workflow_run_id, calculated_at)`
- `cost_entries (project_id, deduplication_key)` unique
- Source-event indexes on `cost_entries`
- `cost_attributions (workflow_run_id, attribution_type)`
- `waste_events (workflow_run_id, waste_type)`

### Comparison and recommendation indexes

- `comparison_runs (workflow_id, created_at DESC)`
- `comparison_runs (configuration_a_id)` and `(configuration_b_id)`
- `recommendations (project_id, recommendation_category, generated_at DESC)`
- `recommendations (workflow_id, generated_at DESC)`
- Partial index for current recommendations

### Audit indexes

- `audit_events (project_id, created_at DESC)`
- `audit_events (organization_id, created_at DESC)`
- `audit_events (actor_user_id, action_type, created_at DESC)`
- `audit_events (entity_type, entity_id)`

### Index restraint

Do not index every column. Indexes increase write and migration cost. Add further indexes only after measuring actual query plans.

---

## 12. Data Validation Rules

### Identity and tenancy

- Email is unique case-insensitively.
- Every project belongs to one organization.
- Every project member must be an active organization member.
- Cross-project foreign-key combinations are rejected by service validation and transaction checks.

### Workflow and contract rules

- One active Outcome Contract per workflow at a time.
- Contract and workflow version numbers are positive and unique within their parent.
- A run references versions belonging to its workflow.
- Referenced versions, configurations and rate cards are immutable.

### Usage and execution rules

- Input and output tokens are non-negative integers.
- Latency is non-negative.
- Model calls and tool calls belong to one workflow run and one run attempt.
- Parent calls and attempts belong to the same run.
- Completion timestamps cannot precede start timestamps.
- Idempotency keys are unique per run.

### Rate and cost rules

- Rates and known costs are non-negative.
- Rate cards require `effective_from`; `effective_to`, when present, is later.
- Model/tool rate cards match the referenced model/tool.
- Cost entries cannot be orphaned from their project and run.
- Exact or estimated event costs reference one source event.
- A model or tool call cannot create duplicate included cost entries.
- Null unknown amount is not converted to zero.
- All included cost entries use the project reporting currency in the MVP.

### Outcome rules

- Technical completion does not set business success automatically.
- Outcome transitions follow the permitted state machine.
- Pending is excluded from finalised success yield.
- Reversed requires an earlier success event.
- Manual verification records actor and source.
- Outcome history is append-only.

### Waste rules

- Waste amount is non-negative.
- Waste references one run, source execution event and cost entry.
- All waste references share the same workflow run.
- Allocated waste cannot exceed the cost entry amount.
- Duplicate allocation of the same cost portion is prohibited.

### Comparison and recommendation rules

- Compared configurations are distinct and belong to the same workflow.
- Comparison end is later than start.
- Sample sizes are non-negative and match stored cohorts.
- Recommendations cannot become current without evidence.
- Insufficient evidence produces `investigate`.
- Recommendation evidence belongs to the same project/workflow context.

### Sensitive-data rules

- Full customer messages, prompts, responses, card numbers, account numbers, bank information and secrets are prohibited.
- External ticket references are synthetic or hashed.
- JSONB evidence is redacted before persistence.
- Audit summaries contain safe field-level descriptions rather than raw payloads.

---

## 13. Demo Data Plan

### 13.1 Tenant and project

- **Organization:** Acme Payments
- **Project:** AI Customer Support
- **Workflow:** Payment Support Resolution
- **Outcome Contract:** Ticket resolved without human escalation and not reopened within 48 hours; unsupported refund claims fail the quality rule.

### 13.2 Providers and models

| Provider | Model | Role in demo | Input rate / 1M | Output rate / 1M |
|---|---|---|---:|---:|
| SimuLean AI | Economy S | Economy-first primary | $1.00 | $3.00 |
| SimuLean AI | Economy M | Secondary economy option | $2.00 | $6.00 |
| SimuPrime AI | Quality S | Quality-first primary and Economy-first fallback | $5.00 | $15.00 |
| SimuPrime AI | Quality Pro | Quality-first fallback | $8.00 | $24.00 |

These are controlled demo rates, not claims about real providers.

### 13.3 Tools

| Tool | Demo unit cost |
|---|---:|
| Payment Status Lookup | $0.0020 per call |
| Transaction History Lookup | $0.0015 per call |
| Refund Policy Lookup | $0.0020 per call |

### 13.4 Workflow configurations

**Economy-first**

- Primary: Economy S
- Fallback: Quality S
- One payment-tool retry
- Fallback after quality-rule rejection

**Quality-first**

- Primary: Quality S
- Fallback: Quality Pro
- Fewer expected retries
- Higher direct call cost

### 13.5 Example ticket

> “My payment failed but money was deducted.”

Only a synthetic ticket reference and category `payment_failure` are stored. The full message is presentation-only demo content and is not required in an operational table.

The representative Economy-first run contains:

1. Economy S primary model call.
2. Payment Status Lookup timeout.
3. Payment Status Lookup retry succeeds.
4. Economy S follow-up is rejected by the quality rule.
5. Quality S fallback succeeds.
6. Refund Policy Lookup confirms the response.
7. Technical run completes.
8. Outcome starts pending and becomes success after verification.

Expected cost and waste evidence:

- Attributed run cost: approximately `$0.01960000`.
- Failed tool waste: `$0.00200000`.
- Superseded response waste: approximately `$0.00126000`.
- Total classified failure waste: approximately `$0.00326000`.

### 13.6 Cohort generation

Generate 200 deterministic synthetic runs using a fixed seed.

| Final current outcome | Economy-first | Quality-first |
|---|---:|---:|
| Success | 55 | 82 |
| Failure | 29 | 9 |
| Pending | 8 | 5 |
| Abandoned | 5 | 2 |
| Reversed | 3 | 2 |
| **Total** | **100** | **100** |

Reversed runs contain at least two outcome events: an earlier success followed by reversal.

Suggested execution volume:

- Economy-first: about 170 model calls, 160 tool calls, 28 retry attempts and 25 fallback attempts.
- Quality-first: about 135 model calls, 145 tool calls, 15 retry attempts and 15 fallback attempts.
- Each successful, failed or timed-out billable call receives one cost entry.
- Each cost entry receives an exact, estimated or unattributed classification.
- Failed and superseded call costs receive non-overlapping waste events.

### 13.7 Economic totals

| Metric | Economy-first | Quality-first |
|---|---:|---:|
| Attempts | 100 | 100 |
| Total known cost | $1.20 | $1.60 |
| Cost per attempt | **$0.01200** | $0.01600 |
| Verified current successes | 55 | 82 |
| Finalised runs | 92 | 95 |
| Finalised success yield | 59.78% | **86.32%** |
| Cost per successful outcome | $0.02182 | **$0.01951** |
| Classified failure waste | $0.47 | $0.29 |
| Pending runs | 8 | 5 |
| Attribution coverage target | ≥95% | ≥95% |

The known cost total includes the cost accumulated by pending runs at the comparison cutoff. Pending counts remain visible and are excluded from finalised success yield.

### 13.8 Comparison and recommendation records

Create one completed `comparison_runs` record containing:

- Same workflow and ticket category
- Same evaluation period
- 100 runs in each cohort
- Calculation version `unit-economics-v1`
- Stored cohort identifiers and metric snapshots

Expected comparison result:

- Economy-first is 25% cheaper than Quality-first when measured per attempt.
- Quality-first is approximately 10.6% cheaper when measured per successful outcome.
- Quality-first has materially higher finalised success yield and lower failure waste.

Create recommendations:

- **Quality-first:** `scale`, high confidence, supported by cost-per-success, success-yield, waste and sample-size evidence.
- **Economy-first:** `restrict` or `optimise`, supported by its higher cost per successful outcome and retry/fallback waste.

This demo directly establishes the project’s primary product proof.

---

## 14. Final Database Summary

This schema is realistic for a three-month MVP because it uses one PostgreSQL database, conventional relational entities and a narrow customer-support domain. It avoids cloud invoice ingestion, enterprise chargeback, universal GPU allocation and sensitive conversation storage.

At the same time, it preserves the evidence expected from an industry-grade financial decision system: immutable contract and workflow versions, effective rate cards, idempotent execution events, append-only outcomes, reproducible cost entries, non-duplicated waste allocation, versioned comparisons, numerical recommendation evidence and redacted audit history.

The database supports OutcomeIQ’s main proof because it can calculate both sides of the decision from the same authoritative evidence. Economy-first can be shown as cheaper per attempt, while Quality-first can be shown as cheaper per verified successful outcome. Neither conclusion depends on a chatbot opinion or an opaque dashboard calculation; both are reproducible from workflow runs, call usage, applicable rates, outcome history, cost entries and comparison evidence.
