# OutcomeIQ — REST API Design

**Project:** OutcomeIQ — Outcome-aware AI FinOps Platform  
**Scope:** Three-month MVP  
**MVP vertical:** AI customer-support ticket resolution  
**Architecture:** FastAPI modular monolith  
**API style:** Versioned JSON REST API  
**Document status:** Design only; no routes, models, migrations or frontend code are created by this document

---

## 1. API Design Overview

The OutcomeIQ API connects product setup, simulated workflow telemetry, deterministic financial calculations and verified business outcomes through one coherent backend contract.

The API supports:

- **Authentication:** Registration, login, refresh, logout and current-user identity.
- **Organization and project setup:** Tenant creation, membership and project-level access control.
- **Workflow registry:** Version-aware management of customer-support workflows.
- **Outcome Contract management:** Versioned definitions of success, failure, pending, abandonment and reversal.
- **Provider and model setup:** Simulated providers, models and effective token-rate cards.
- **Workflow configuration:** Economy-first and Quality-first model, retry and tool policies.
- **Workflow run tracking:** Creation, technical completion, abandonment and timeline retrieval.
- **Model and tool logging:** Idempotent ingestion of token, latency, retry, fallback and error evidence.
- **Cost calculation:** Deterministic cost entries, attribution classifications and reproducible summaries.
- **Outcome reconciliation:** Business outcome history independent of technical completion.
- **Failure-waste analysis:** Evidence-backed classification of failed or superseded cost.
- **Configuration comparison:** Reproducible cohort comparisons using the same workflow, period and ticket category.
- **Recommendations:** Rule-based Scale, Keep, Optimise, Investigate, Restrict or Stop decisions.
- **Dashboard analytics:** Unit economics, outcome distribution, cost trends, waste and model performance.
- **Auditability:** Read access to significant membership, contract, rate, outcome, calculation and recommendation actions.

### API boundary

The API does not call real AI providers in the MVP. A simulated support workflow posts completed model-call and tool-call events. OpenAI, Gemini, Claude and Ollama adapters can later emit the same event contract.

### Important supporting assumptions

1. The database design’s `project_members` table is used for authorization.
2. Refresh-token rotation and logout revocation require a small security-supporting `auth_sessions` record, stored as a hashed refresh-token identifier. This is an implementation addendum to the domain-focused database document.
3. Providers remain organization-owned in PostgreSQL. Project-scoped provider routes use the project as the authorization context and return providers belonging to its organization.
4. Recommendation accept/reject in the MVP records an audited review decision. It does not change routing or deploy a configuration.

---

## 2. API Design Principles

### 2.1 RESTful structure

Resources use nouns, hierarchical routes only where ownership is meaningful, and action routes for lifecycle operations that are not simple field updates.

Examples:

- `/projects/{project_id}/workflows` expresses project ownership.
- `/runs/{run_id}/outcomes` expresses outcome history belonging to a run.
- `/workflows/{workflow_id}/activate` expresses a controlled state transition.

### 2.2 Versioned API prefix

All product APIs use `/api/v1`. Health and readiness endpoints remain unversioned because they are infrastructure probes.

### 2.3 JWT authentication

Protected endpoints accept a short-lived bearer access token. Refresh tokens are rotated and revocable. Tokens identify the user; database membership determines authorization.

### 2.4 Project-level authorization

Every project-owned request must verify:

1. The authenticated user is active.
2. The resource belongs to a project.
3. The user has an active `project_members` record, or is an authorized organization owner.
4. The assigned role permits the operation.

Resource-not-found responses should not reveal the existence of another project’s data.

### 2.5 Pydantic validation

Request and response objects validate identifiers, timestamps, enum values, monetary precision, non-negative usage and maximum text lengths. Domain validation remains in services rather than route handlers.

### 2.6 Deterministic backend calculations

All authoritative cost, yield, waste, comparison and recommendation calculations occur in backend services using versioned rules. The frontend receives values and calculation metadata; it does not recreate formulas.

### 2.7 Safe errors

Errors return stable machine-readable codes, safe messages and a request identifier. Stack traces, SQL messages, secrets and cross-tenant identifiers are never returned.

### 2.8 Idempotent telemetry ingestion

Model-call and tool-call creation accept an `Idempotency-Key` header. Repeating the same key for the same run and equivalent payload returns the original resource. Reusing it with a different payload returns `409 Conflict`.

### 2.9 Sensitive-data redaction

The API accepts synthetic or opaque ticket references, hashes them before storage where appropriate, and rejects prohibited payment or credential fields. Prompt hashes may be supplied; full prompts and customer conversations are not part of the MVP contract.

### 2.10 Time, currency and precision

- Timestamps use ISO 8601 with timezone and are normalized to UTC.
- Monetary responses are decimal strings, not binary floating-point numbers.
- The MVP uses one project reporting currency.
- Token and latency values are non-negative integers.

### 2.11 Pagination and filtering

List endpoints use `page` and `page_size` for MVP simplicity. Default page size is 25 and maximum is 100. Time-based analytics accept `from`, `to`, `ticket_category` and configuration filters where relevant.

---

## 3. Authentication APIs

| Endpoint | Purpose and authentication | Request body | Response body | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/auth/register` | Compatibility alias that sends registration email OTP. No authentication required. Does not activate immediately. | `email`, `password`, `full_name` | `message` | Valid email; password length; bounded name. `409 email_already_registered`, `429 otp_cooldown`, `422 validation_error` |
| `POST /api/v1/auth/register/request-otp` | Sends or safely resends registration email OTP. No authentication required. | `email`, `password`, `full_name` | `message` | Stores only hashed OTP; pending OTP expires after configured window. `409 email_already_registered`, `429 otp_cooldown`, `422 validation_error` |
| `POST /api/v1/auth/register/verify-otp` | Verifies OTP and creates active user after human-entered code matches. No authentication required. | `email`, `otp` | User profile | Max 5 wrong attempts; expired codes require a new OTP. `400 invalid_or_expired_otp`, `409 email_already_registered`, `429 too_many_attempts`, `422 validation_error` |
| `POST /api/v1/auth/login` | Authenticates an existing user. No authentication required. | `email`, `password` | User identity, access token, refresh token, expiry metadata | Generic invalid-credential response; inactive users rejected. `401 invalid_credentials`, `403 account_inactive` |
| `POST /api/v1/auth/logout` | Revokes the presented refresh session. Access or refresh authentication required. | Refresh token or session identifier, depending on transport decision | Revocation confirmation and timestamp | Token must belong to caller. `401 invalid_token`, `409 session_already_revoked` |
| `GET /api/v1/auth/me` | Returns the current identity and accessible roles. Access token required. | None | User profile, organization memberships and project memberships | `401 missing_or_expired_token` |
| `POST /api/v1/auth/refresh` | Rotates a valid refresh token. Refresh authentication required. | Refresh token | New access token, rotated refresh token and expiries | Reuse of rotated token revokes the session family. `401 invalid_refresh_token`, `409 refresh_token_reused` |

### Authentication response rule

Password hashes, refresh-token hashes and internal security state are never returned. Authentication failures use generic wording to reduce account enumeration.

---

## 4. Organization and Project APIs

### 4.1 Organization endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/organizations` | Creates an organization. Any authenticated user; creator becomes organization owner. | `name`, optional `slug`, `default_currency`, `timezone` | Organization and caller membership | Unique slug; valid currency/timezone. `409 slug_conflict`, `422 validation_error` |
| `GET /api/v1/organizations` | Lists organizations accessible to the caller. Authenticated. | Pagination and optional active filter | Paginated organization summaries and caller roles | `401 unauthorized` |
| `GET /api/v1/organizations/{organization_id}` | Reads organization details. Organization member. | Path identifier | Organization details and caller role | `403 forbidden` or tenant-safe `404 not_found` |
| `POST /api/v1/organizations/{organization_id}/members` | Adds or updates an organization member. Organization owner/admin. | `user_id` or `email`, `role` | Membership record | User must exist; owner-demotion protections. `403`, `404 user_not_found`, `409 membership_conflict` |

### 4.2 Project endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/projects` | Creates a project under an organization. Organization owner/admin. | `organization_id`, `name`, optional `slug`, `description`, `currency`, `timezone` | Project plus creator’s `project_owner` membership | Caller must manage organization; currency is fixed after financial evidence exists. `403`, `409 slug_conflict`, `422` |
| `GET /api/v1/projects` | Lists projects accessible to the caller. Authenticated. | Pagination, optional `organization_id`, `is_active` | Paginated project summaries with caller role | `403` for inaccessible organization filters |
| `GET /api/v1/projects/{project_id}` | Reads project details. Project member or organization owner. | Path identifier | Project details and access role | `403` or tenant-safe `404` |
| `PUT /api/v1/projects/{project_id}` | Updates safe project metadata. Project owner. | Optional `name`, `description`, `timezone`, `is_active` | Updated project | Currency immutable after first cost entry. `403`, `409 immutable_currency`, `422` |
| `DELETE /api/v1/projects/{project_id}` | Archives a project; never hard-deletes financial evidence. Project owner. | Optional `reason` | Archived status and timestamp | `409 already_archived`; active processing may require confirmation |

### 4.3 Necessary project-member endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `GET /api/v1/projects/{project_id}/members` | Lists project access. Project owner; organization owner. | Pagination | Memberships and roles | `403` |
| `POST /api/v1/projects/{project_id}/members` | Grants project access. Project or organization owner. | `user_id` or `email`, `role` | Created membership | User must belong to organization. `409 membership_conflict`, `422 invalid_project_role` |
| `DELETE /api/v1/projects/{project_id}/members/{user_id}` | Revokes project access. Project or organization owner. | Optional `reason` | Revocation confirmation | Cannot remove final project owner. `409 final_owner` |

### Project access rules

- Organization owners may administer projects in their organization.
- Project owners manage project membership and all project resources.
- Editors manage workflows, telemetry, outcomes and calculations.
- Analysts read source evidence and generate derived comparisons/recommendations.
- Viewers have read-only product access.
- Membership changes generate audit events.

---

## 5. Workflow Registry APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/projects/{project_id}/workflows` | Creates a workflow and version 1. Project owner/editor. | `name`, `slug`, `category`, `description`, optional `business_owner_user_id`, `technical_owner_user_id`, version definition | Workflow, version 1 and status `draft` | Owners must be project members; unique slug. `409 workflow_slug_conflict`, `422` |
| `GET /api/v1/projects/{project_id}/workflows` | Lists project workflows. Any project member. | Pagination; filters `status`, `category`, `owner` | Paginated workflow summaries and current version | `403` |
| `GET /api/v1/workflows/{workflow_id}` | Returns workflow, versions and active dependencies. Any project member. | Path identifier | Workflow details, latest version, contract/configuration counts | `404` |
| `PUT /api/v1/workflows/{workflow_id}` | Updates metadata or creates a new workflow version when semantic definition changes. Project owner/editor. | Metadata fields; optional version definition and `change_summary` | Updated workflow and new/current version | Referenced versions immutable. `409 version_conflict`, `422` |
| `POST /api/v1/workflows/{workflow_id}/activate` | Activates a draft or paused workflow. Project owner/editor. | Optional `reason` | Active workflow status | Requires active contract and configuration. `409 workflow_not_ready` |
| `POST /api/v1/workflows/{workflow_id}/deactivate` | Pauses new runs while preserving history. Project owner/editor. | `reason` | Paused workflow status | Existing runs remain accessible. `409 already_paused` |

### Workflow versioning rule

Changing display metadata may update the workflow record. Changing business definition, category semantics or execution meaning creates a new immutable workflow version. Runs continue referencing the version selected at start.

---

## 6. Outcome Contract APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/workflows/{workflow_id}/outcome-contracts` | Creates a draft contract and version 1. Project owner/editor. | `name`, `unit_of_work`, success/failure/pending/abandoned/reversed criteria, `finalization_window_hours`, `verification_source`, `quality_rules` | Contract and version 1 | All five state definitions required; window non-negative. `409 contract_name_conflict`, `422` |
| `GET /api/v1/workflows/{workflow_id}/outcome-contracts` | Lists current and historical contracts. Any project member. | Pagination; optional `status` | Contracts, active version and version counts | `403`, `404` |
| `GET /api/v1/outcome-contracts/{contract_id}` | Reads a contract with version history. Any project member. | Path identifier | Contract and ordered versions | `404` |
| `POST /api/v1/outcome-contracts/{contract_id}/versions` | Creates a new immutable version. Project owner/editor. | Full contract definition plus `change_summary` | New draft version | Cannot partially inherit ambiguous criteria; version generated by server. `409 duplicate_version`, `422` |
| `POST /api/v1/outcome-contract-versions/{version_id}/activate` | Activates a version and its contract. Project owner/editor. | `reason` | Active contract/version and retired prior active contract status | Only one active contract per workflow. `409 active_contract_conflict`, `422 invalid_contract` |

### Contract response fields

Responses expose:

- Unit of work
- Success, failure, pending, abandoned and reversed definitions
- Finalization window
- Verification source
- Quality rules
- Contract status
- Version number
- Active version indicator
- Created-by and created-at metadata

Activation and version creation generate audit events.

---

## 7. Provider, Model and Rate Card APIs

### 7.1 Provider endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/projects/{project_id}/providers` | Creates an organization-owned provider using project authorization context. Project owner/editor. | `name`, `provider_key`, `is_simulated`, `is_active`, safe metadata | Provider identity and owning organization | Unique provider key within organization; metadata rejects secrets. `409 provider_conflict`, `422` |
| `GET /api/v1/projects/{project_id}/providers` | Lists providers available to the project. Any project member. | Pagination; filters `is_active`, `is_simulated` | Provider summaries | `403` |

### 7.2 Model endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/providers/{provider_id}/models` | Registers a simulated model. Project owner/editor in an authorized project context. | `model_key`, `display_name`, optional `model_family`, `is_active`, `capabilities` | Model record | Provider access required; unique model key. `409 model_conflict`, `422` |
| `GET /api/v1/providers/{provider_id}/models` | Lists provider models. Project member with provider access. | Pagination; optional `is_active` | Model summaries | `403`, `404` |

Because provider routes are organization-scoped in storage, callers supply an authorized project context through a standard `X-Project-Id` header for direct provider/model routes. The backend verifies that the project belongs to the provider’s organization.

### 7.3 Model rate-card endpoints

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/models/{model_id}/rate-cards` | Adds an immutable effective token rate. Project owner/editor. | `currency`, `input_price_per_million`, `output_price_per_million`, optional `fixed_call_price`, `effective_from`, optional `effective_to`, `source`, `is_estimated` | Created rate card | Non-negative rates; project currency match; no overlapping effective period. `409 rate_overlap`, `422` |
| `GET /api/v1/models/{model_id}/rate-cards` | Lists historical and current rates. Any authorized project member. | Pagination; optional `effective_at`, `active_only` | Ordered rate cards and current indicator | `403`, `404` |

Historical rate cards are never edited through the API. A price change creates a new effective record.

---

## 8. Tool and Tool Rate APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/projects/{project_id}/tools` | Registers a project tool. Project owner/editor. | `tool_key`, `display_name`, `description`, `is_active`, safe metadata | Tool record | Unique project tool key; no credentials. `409 tool_conflict`, `422` |
| `GET /api/v1/projects/{project_id}/tools` | Lists project tools. Any project member. | Pagination; optional `is_active` | Tool summaries | `403` |
| `POST /api/v1/tools/{tool_id}/rate-cards` | Adds immutable tool pricing. Project owner/editor. | `currency`, `unit_name`, `unit_price`, `effective_from`, optional `effective_to`, `source`, `is_estimated` | Created rate card | Non-negative price; valid period; no overlap. `409 rate_overlap`, `422` |
| `GET /api/v1/tools/{tool_id}/rate-cards` | Lists tool-rate history. Any project member. | Pagination; optional `effective_at` | Ordered rate cards | `403`, `404` |

### MVP tool seed values

- Payment Status Service
- Transaction History Service
- Refund Policy Service

Tools store operational identifiers and economic metadata, never credentials or payment responses.

---

## 9. Workflow Configuration APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/workflows/{workflow_id}/configurations` | Creates a draft configuration. Project owner/editor. | `name`, `configuration_key`, `workflow_version_id`, `primary_model_id`, optional `fallback_model_id`, `retry_policy`, `tool_policy`, optional `effective_from`, `effective_to` | Configuration with model-role mappings | Models must be active and available; primary required; valid period. `409 configuration_conflict`, `422` |
| `GET /api/v1/workflows/{workflow_id}/configurations` | Lists configurations. Any project member. | Pagination; optional `status`, `effective_at` | Configuration summaries | `403` |
| `GET /api/v1/configurations/{configuration_id}` | Reads a configuration and policies. Any project member. | Path identifier | Models, retry/tool policy, status and usage count | `404` |
| `PUT /api/v1/configurations/{configuration_id}` | Updates an unused draft configuration. Project owner/editor. | Mutable configuration fields | Updated draft | Once referenced by a run, configuration is immutable; create a new configuration instead. `409 configuration_in_use` |
| `POST /api/v1/configurations/{configuration_id}/activate` | Activates a ready configuration. Project owner/editor. | Optional `reason` | Active status and effective period | Requires primary model and applicable rate card. `409 configuration_not_ready` |
| `POST /api/v1/configurations/{configuration_id}/deactivate` | Pauses new run selection. Project owner/editor. | `reason` | Paused status | Historical runs unaffected. `409 already_inactive` |

Economy-first and Quality-first are separate immutable configurations, not mutable modes of one row.

---

## 10. Workflow Run APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/workflows/{workflow_id}/runs/start` | Starts one simulated ticket workflow. Project owner/editor or authorized demo actor. | `external_ticket_reference`, `ticket_category`, `configuration_id`, optional `outcome_contract_version_id`, optional `correlation_id`, safe metadata | Run ID, frozen workflow/configuration/contract versions, correlation ID and initial statuses | Active workflow/configuration required; ticket reference bounded and hashed; correlation unique. `409 workflow_not_active`, `409 duplicate_correlation`, `422` |
| `GET /api/v1/workflows/{workflow_id}/runs` | Lists runs for a workflow. Any project member. | Pagination; filters for configuration, run status, technical status, outcome status, ticket category and date range | Paginated run summaries | Valid range and filter enums. `422` |
| `GET /api/v1/runs/{run_id}` | Reads complete run summary. Any project member. | Path identifier | Frozen references, statuses, usage counts, cost summary and current outcome | `404` |
| `GET /api/v1/runs/{run_id}/timeline` | Returns an ordered combined timeline. Any project member. | Optional event-type filters | Status, attempt, model, tool, outcome, cost and waste events with safe evidence | `404` |
| `POST /api/v1/runs/{run_id}/complete` | Marks technical processing complete; does not declare business success. Project owner/editor. | `technical_status`, optional `completed_at`, `reason` | Updated technical/run state and current independent outcome | Technical status must be terminal. `409 invalid_run_transition`, `422` |
| `POST /api/v1/runs/{run_id}/abandon` | Cancels execution and explicitly records an abandoned business outcome. Project owner/editor. | `reason`, `verification_source`, optional redacted evidence reference | Cancelled technical state plus appended abandoned outcome | Cannot abandon already finalised success without reversal flow. `409 invalid_run_transition` |

### Run status separation

- `run_status` describes lifecycle: created, running, completed or cancelled.
- `technical_status` describes execution result.
- `outcome_status` describes business result and is controlled through outcome events.

Completing a run never automatically sets success.

---

## 11. Model-Call Logging APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/runs/{run_id}/model-calls` | Records one completed simulated model call and calculates its cost. Project owner/editor; `Idempotency-Key` required. | `model_id`, optional `run_attempt_id`, `sequence_number`, `input_tokens`, `output_tokens`, `latency_ms`, `status`, optional `retry_of_model_call_id`, `fallback_for_model_call_id`, `redacted_prompt_hash`, `error_category`, start/end timestamps | Model-call record, selected rate-card reference, cost entry, attribution type and calculation version | Non-negative usage; model allowed by configuration; only one retry/fallback parent; parent in same run; no full prompt. `409 idempotency_conflict`, `409 invalid_call_parent`, `422` |
| `GET /api/v1/runs/{run_id}/model-calls` | Lists model calls in execution order. Any project member. | Pagination; optional status/model filters | Calls with usage, rate and cost summaries | `404` |
| `GET /api/v1/model-calls/{model_call_id}` | Reads one call and its economic evidence. Any project member. | Path identifier | Call, parent relationship, rate card, cost and waste links | `404` |

### Model-call cost behaviour

The backend selects the rate effective at call start. If no valid rate exists, the call may be stored but receives an unattributed or estimated cost state rather than an invented zero amount.

---

## 12. Tool-Call Logging APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/runs/{run_id}/tool-calls` | Records a simulated tool call and its cost. Project owner/editor; `Idempotency-Key` required. | `tool_id`, optional `run_attempt_id`, `sequence_number`, `units`, `latency_ms`, `status`, optional `retry_of_tool_call_id`, optional `manual_cost`, `currency`, `cost_source`, `error_category`, timestamps | Tool-call record, rate or manual-cost evidence, cost entry and attribution type | Tool permitted by configuration; non-negative values; retry parent in same run. Manual cost defaults to estimated unless independently verified. `409 idempotency_conflict`, `422` |
| `GET /api/v1/runs/{run_id}/tool-calls` | Lists tool calls in order. Any project member. | Pagination; optional tool/status filters | Calls with rate, cost and retry summaries | `404` |
| `GET /api/v1/tool-calls/{tool_call_id}` | Reads a tool call and linked cost/waste evidence. Any project member. | Path identifier | Tool call, parent relationship, cost and waste links | `404` |

Tool responses and payment information are never accepted as persistent payload fields. Safe result categories may be included in redacted evidence.

---

## 13. Cost Calculation APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/runs/{run_id}/costs/recalculate` | Recomputes cost evidence using the current calculation service while preserving version history. Project owner/editor. | `reason`; optional `include_incomplete_calls=false` | Calculation version, recalculated entries, totals, differences and audit reference | Reason required; run and rates valid. `409 calculation_in_progress`, `422` |
| `GET /api/v1/runs/{run_id}/costs` | Lists authoritative cost entries and attribution records. Any project member. | Pagination; optional `cost_type`, `attribution_type`, `calculation_version` | Cost entries, sources, rates and attribution evidence | `404` |
| `GET /api/v1/runs/{run_id}/cost-summary` | Returns one reproducible run-level cost envelope. Any project member. | Optional calculation version; defaults current | Base totals, diagnostic subsets, attribution breakdown, unknown items and formula metadata | `404`, `409 no_current_calculation` |

### Required cost-summary fields

- `model_cost`
- `tool_cost`
- `external_api_cost`
- `direct_compute_cost`
- `total_known_cost`
- `retry_cost`
- `fallback_cost`
- `attributed_cost`
- `estimated_cost`
- `unattributed_known_cost`
- `unknown_cost_entry_count`
- `attribution_coverage`
- `coverage_method`
- `currency`
- `calculation_version`
- `calculated_at`

### Non-additive breakdown rule

`model_cost`, `tool_cost`, `external_api_cost` and `direct_compute_cost` are mutually exclusive base totals. `retry_cost` and `fallback_cost` are diagnostic subsets of those totals and must be labelled `non_additive=true`. Similarly, exact/estimated/unattributed is an attribution view over the same costs. The frontend must never add all displayed fields together.

Unknown amount remains null with a visible count and reason; it is not converted to zero.

---

## 14. Outcome APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/runs/{run_id}/outcomes` | Appends a pending, success, failure or abandoned outcome event. Project owner/editor. | `outcome_status`, `verification_source`, optional `occurred_at`, `reason`, `evidence_reference`, `quality_status` | Outcome event, current outcome and finalisation status; `verified_by` and `verified_at` server-derived | Valid transition; success/failure require verification; evidence redacted. `409 invalid_outcome_transition`, `422` |
| `GET /api/v1/runs/{run_id}/outcomes` | Lists append-only outcome history. Any project member. | Pagination | Ordered outcome events and verification metadata | `404` |
| `GET /api/v1/runs/{run_id}/current-outcome` | Returns current business outcome. Any project member. | None | Current status, verified state, source, finalisation and preceding event | `404` |
| `POST /api/v1/runs/{run_id}/outcomes/reverse` | Reverses a verified success while preserving history. Project owner/editor. | `verification_source`, `reason`, `evidence_reference`, optional `occurred_at`, `quality_status` | Reversal event and current reversed outcome | Current state must be success; manual actor derived from JWT. `409 outcome_not_reversible`, `422` |

### Outcome rules

- `verified_by` is derived from the authenticated actor and cannot impersonate another user.
- Pending may be unverified; success, failure and reversal require a verification source.
- Pending outcomes are excluded from finalised success yield.
- Reversal appends history and never edits the success event.
- `quality_status` is one of `passed`, `failed`, `not_evaluated` and does not replace outcome status.

---

## 15. Failure-Waste APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/runs/{run_id}/waste-events/classify` | Runs deterministic waste-classification rules for one run. Project owner/editor. | Optional `classification_version`; optional `replace_current=false`; `reason` for manual rerun | Created/current waste events, total waste, percentage, confidence and evidence links | Run must have cost evidence; classification idempotent per version. `409 classification_in_progress`, `422 missing_cost_evidence` |
| `GET /api/v1/runs/{run_id}/waste-events` | Lists run waste evidence. Any project member. | Pagination; optional `waste_type`, `confidence_level` | Waste events, source calls, cost entries and reasons | `404` |
| `GET /api/v1/workflows/{workflow_id}/waste-summary` | Aggregates mutually exclusive waste amounts. Any project member. | Date range, optional configuration and ticket category | Waste total, percentage, type breakdown, affected runs and calculation metadata | `422 invalid_range` |

Supported types:

- `failed_model_call`
- `failed_tool_call`
- `retry_caused_by_failure`
- `superseded_response`
- `unproductive_fallback`
- `failed_workflow_run`

Waste classification never changes run cost. It allocates part of existing cost to an evidence-backed diagnostic category.

---

## 16. Dashboard and Analytics APIs

All analytics responses include `from`, `to`, timezone, currency, calculation version, pending count, attribution coverage and data-freshness timestamp.

| Endpoint | Purpose and access | Query | Response | Validation and possible errors |
|---|---|---|---|---|
| `GET /api/v1/projects/{project_id}/dashboard/summary` | Project-level decision overview. Any project member. | Date range; optional workflow/configuration/category | Workflow counts, attempts, outcomes, costs, waste, coverage and current recommendations | `422 invalid_range` |
| `GET /api/v1/workflows/{workflow_id}/analytics/unit-economics` | Returns authoritative unit economics. Any project member. | Date range; optional configuration/category | Total attempts, finalised attempts, successes, failures, pending, abandoned, reversed, success yield, average cost per attempt, cost per successful outcome, waste and latency | `409 insufficient_data` may return data with eligibility false rather than fail |
| `GET /api/v1/workflows/{workflow_id}/analytics/cost-trend` | Time-series cost view. Any project member. | Date range, `bucket=day|week`, optional filters | Bucketed known cost, unknown count, attempts and cost-per-attempt | `422` |
| `GET /api/v1/workflows/{workflow_id}/analytics/outcome-distribution` | Outcome-state distribution. Any project member. | Date range and filters | Counts and percentages by current outcome plus historical reversal count | `422` |
| `GET /api/v1/workflows/{workflow_id}/analytics/failure-waste` | Waste analytics. Any project member. | Date range and filters | Mutually exclusive waste totals and type breakdown | `422` |
| `GET /api/v1/workflows/{workflow_id}/analytics/model-performance` | Economic and outcome metrics by model. Any project member. | Date range, optional model/configuration/category | Calls, tokens, cost, latency, failed calls and associated run outcomes | `422` |

### Metric definitions

- **Total attempts:** Valid runs started in the selected cohort.
- **Finalised attempts:** Current success, failure, abandoned or reversed outcomes.
- **Success yield:** Current successes divided by finalised attempts.
- **Average cost per attempt:** Known included cost divided by valid attempts.
- **Cost per successful outcome:** Known included cohort cost divided by verified current successes. Pending cost included at the selected cutoff is disclosed separately so the interpretation remains transparent.
- **Failure waste:** Mutually exclusive classified waste amount, not a second charge.
- **Attribution coverage:** Calculated using the stated coverage method; unknown amounts remain visible.
- **Average latency:** Run or call latency as explicitly identified by the response field.

If no verified success exists, cost per successful outcome is `null` with reason `no_successful_outcomes`, never zero.

---

## 17. Configuration Comparison APIs

| Endpoint | Purpose and access | Request/query | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/workflows/{workflow_id}/comparisons` | Creates a reproducible comparison snapshot. Project owner/editor/analyst. | `configuration_a_id`, `configuration_b_id`, `from`, `to`, optional `ticket_category`, `minimum_sample_size`, optional inclusion policy | Comparison ID, stored cohorts, sample sizes, metrics A/B, eligibility and insufficiency reasons | Configurations distinct and same workflow; range valid; no cross-category comparison unless requested. `409 incomparable_configurations`, `422` |
| `GET /api/v1/comparisons/{comparison_id}` | Reads one comparison snapshot. Any project member. | Path identifier | Filters, cohorts, all metrics, calculation version and recommendation eligibility | `404` |
| `GET /api/v1/workflows/{workflow_id}/comparisons` | Lists historical comparisons. Any project member. | Pagination; optional configuration/date/status filters | Comparison summaries | `403` |

### Required comparison metrics

For each configuration:

- Sample size
- Total and finalised attempts
- Pending count
- Cost per attempt
- Success yield
- Cost per successful outcome
- Failure-waste amount and percentage
- Attribution coverage
- Average latency

The response includes `recommendation_eligible`, `eligibility_checks` and any insufficiency reasons. Cohort run identifiers are frozen at comparison creation for reproducibility.

---

## 18. Recommendation APIs

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/comparisons/{comparison_id}/recommendations/generate` | Applies the active deterministic rule set. Project owner/editor/analyst. | Optional `reason`; rule version selected by server | Recommendation with category, target, confidence, rule/calculation versions, sample size, metrics, evidence links, reason and generation time | If comparison is insufficient, result must be Investigate. `409 recommendation_generation_conflict`, `422` |
| `GET /api/v1/recommendations/{recommendation_id}` | Reads one recommendation and all evidence. Any project member. | Path identifier | Complete recommendation, supporting metrics, source links and review state | `404` |
| `GET /api/v1/workflows/{workflow_id}/recommendations` | Lists current and historical recommendations. Any project member. | Pagination; filters category, confidence, current-only | Recommendation summaries | `403` |
| `POST /api/v1/recommendations/{recommendation_id}/accept` | Records human acceptance; does not change routing. Project owner/editor. | `reason` | Recommendation plus accepted review audit event | Cannot accept insufficient Investigate as a deployment decision. `409 recommendation_not_actionable` |
| `POST /api/v1/recommendations/{recommendation_id}/reject` | Records human rejection. Project owner/editor. | `reason` | Recommendation plus rejected review audit event | Reason required. `409 already_reviewed` if single-review policy is used |

### Recommendation categories

- `scale`
- `keep`
- `optimise`
- `investigate`
- `restrict`
- `stop`

### Required recommendation response

- Category and optional target configuration
- Confidence level
- Rule version
- Calculation version
- Comparison period
- Sample size for both cohorts
- Supporting metrics
- Evidence links
- Human-readable reason
- Generated timestamp
- Review state derived from audited accept/reject action

Acceptance is a governance annotation only. Autonomous routing is outside the MVP.

---

## 19. Audit APIs

| Endpoint | Purpose and access | Query | Response | Validation and possible errors |
|---|---|---|---|---|
| `GET /api/v1/projects/{project_id}/audit-events` | Lists redacted project audit history. Organization/project owner; analyst may read if explicitly allowed. | Pagination; date range; optional actor, action and entity filters | Audit summaries | `403`, `422 invalid_range` |
| `GET /api/v1/audit-events/{audit_event_id}` | Reads one safe audit record. Authorized owner/analyst. | Path identifier | Actor, action, entity, timestamp, reason and redacted before/after summaries | `403`, `404` |

Required audited actions include:

- Contract creation, versioning and activation
- Model and tool rate creation
- Outcome verification and reversal
- Manual cost recalculation
- Waste classification rerun
- Comparison and recommendation generation
- Recommendation acceptance/rejection
- Organization and project membership changes

Audit APIs never expose password, token, prompt, customer or secret data.

---

## 20. Demo Data APIs

These endpoints exist only when `DEMO_MODE=true`. Production startup must fail closed if demo routes are accidentally enabled in an unapproved environment.

| Endpoint | Purpose and access | Request | Response | Validation and possible errors |
|---|---|---|---|---|
| `POST /api/v1/demo/seed` | Creates deterministic Acme Payments demo data. Organization/project owner in demo mode. | Optional fixed `seed`, `replace_existing=false` | Counts of created entities, runs and evidence | `403 demo_disabled`, `409 demo_already_seeded` |
| `POST /api/v1/demo/reset` | Removes only records tagged with the isolated demo dataset identifier. Organization/project owner in demo mode. | `confirmation`, demo dataset identifier | Deleted demo counts | Must never delete non-demo data. `403`, `409 unsafe_demo_reset` |
| `POST /api/v1/demo/run-payment-ticket-scenario` | Executes the representative synthetic ticket flow. Project owner/editor in demo mode. | `configuration_id`, optional deterministic failure pattern | Run, timeline, costs, outcome and waste evidence | Configuration must be demo-owned. `403`, `422` |

Demo endpoints generate synthetic references and never accept real payment data.

---

## 21. System APIs

| Endpoint | Authentication | Purpose and response |
|---|---|---|
| `GET /health` | None | Lightweight process-liveness response. Does not query dependencies. |
| `GET /ready` | None or restricted by hosting platform | Readiness result for PostgreSQL, migration state and essential configuration. Redis failure is degraded but not fatal when caching is optional. |
| `GET /api/v1/system/version` | Authenticated | Application version, API version, calculation versions and environment name; no secrets or dependency credentials. |

Infrastructure probes return minimal responses and never include stack traces.

---

## 22. Standard Response Format

### 22.1 Success response

Every successful product response contains:

```text
data: resource, collection or calculated result
meta:
  request_id
  api_version
  generated_at
  optional calculation_version/data_freshness
```

Create operations generally return `201 Created`; reads and actions return `200 OK`. Archive/delete-style actions may return `200` with the resulting state rather than an empty response.

### 22.2 Error response

```text
error:
  code: stable machine-readable identifier
  message: safe human-readable explanation
  details: optional safe field or domain details
  request_id: correlation identifier
```

No internal exception type, SQL statement or cross-tenant identifier is returned.

### 22.3 Pagination format

```text
data: list of resources
meta:
  page
  page_size
  total_items
  total_pages
  request_id
```

Sorting uses an explicit `sort` field from an allowlist. Default event sorting is newest first except timelines, which are chronological.

### 22.4 Validation error format

Validation errors use `422` and include safe field-level entries:

```text
error.code: validation_error
error.details:
  - field
  - rule
  - message
```

Submitted secrets or prohibited sensitive fields are not echoed back.

### 22.5 Decimal and null conventions

- Monetary decimals are returned as strings such as `"0.01951000"`.
- Unknown metrics are `null` with a companion reason.
- Empty collections are arrays, not null.
- Enum values use lowercase database-compatible strings.

---

## 23. Authorization Matrix

Legend: **M** manage/write, **A** analytics-derived write, **R** read, **—** no access. Organization owners have access only within their organization.

| API group | Organization owner | Project owner | Editor | Analyst | Viewer |
|---|---:|---:|---:|---:|---:|
| Authentication | Own account | Own account | Own account | Own account | Own account |
| Organizations | M | R | R | R | R |
| Organization membership | M | — | — | — | — |
| Projects | M | M | R | R | R |
| Project membership | M | M | — | — | — |
| Workflow registry | M | M | M | R | R |
| Outcome Contracts | M | M | M | R | R |
| Providers/models/rates | M | M | M | R | R |
| Tools/rates | M | M | M | R | R |
| Configurations | M | M | M | R | R |
| Run lifecycle | M | M | M | R | R |
| Model/tool logging | M | M | M | R | R |
| Outcome recording/reversal | M | M | M | R | R |
| Cost recalculation | M | M | M | R | R |
| Analytics/dashboard | R | R | R | R | R |
| Comparisons | A | A | A | A | R |
| Recommendation generation | A | A | A | A | R |
| Recommendation accept/reject | M | M | M | R | R |
| Audit logs | R | R | — | Conditional R | — |
| Demo seed/reset | M in demo | M in demo | — | — | — |
| Demo scenario execution | M in demo | M in demo | M in demo | — | — |

### Authorization implementation rule

Authorization is evaluated by the backend on every request. The frontend may hide actions for usability, but hidden controls are not a security boundary.

---

## 24. API Error Handling Strategy

| HTTP status | Use | Example OutcomeIQ codes |
|---|---|---|
| `400 Bad Request` | Syntactically valid request with an unsupported operation not covered by field validation | `invalid_operation`, `unsafe_demo_reset` |
| `401 Unauthorized` | Missing, invalid, expired or revoked authentication | `missing_token`, `invalid_token`, `invalid_credentials` |
| `403 Forbidden` | Authenticated user lacks role or project access | `project_access_denied`, `operation_forbidden`, `demo_disabled` |
| `404 Not Found` | Resource absent or intentionally hidden across tenant boundary | `workflow_not_found`, `run_not_found` |
| `409 Conflict` | State, uniqueness, idempotency or lifecycle conflict | `idempotency_conflict`, `invalid_outcome_transition`, `configuration_in_use`, `rate_overlap` |
| `422 Unprocessable Entity` | Request/field/domain validation failure | `validation_error`, `invalid_date_range`, `negative_tokens` |
| `500 Internal Server Error` | Unexpected server fault | `internal_error` |

### Additional handling rules

- Every error has a request ID.
- Unexpected failures are logged with safe context.
- Database constraint violations are translated into domain errors.
- Cross-tenant access may return `404` to prevent resource enumeration.
- A failed financial transaction rolls back completely.
- Retryable server errors may include a safe `retryable` flag; they do not expose infrastructure details.

---

## 25. API Design Risks and Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Too many endpoints | Three-month implementation becomes fragmented | Implement in vertical slices: setup, run ingestion, outcomes/costs, analytics/comparison. Defer nonessential list filters. |
| Incorrect authorization | Cross-project data exposure | Central project-access dependency, tenant-safe lookups and authorization tests for every route group. |
| Duplicate telemetry ingestion | Cost is counted twice | Required idempotency keys, stable source identifiers and database uniqueness constraints. |
| Inconsistent financial calculations | Dashboard and run details disagree | One cost service and one analytics service; frontend receives calculated values only. |
| Retry/fallback double counting | Total cost is inflated | Treat retry/fallback values as non-additive diagnostic subsets of model/tool totals. |
| Sensitive-data exposure | Privacy and security failure | Strict request allowlists, redaction, size limits, synthetic ticket references and no prompt/message fields. |
| Frontend performs backend calculations | Different screens show different economics | Return all authoritative metrics, formula metadata and calculation versions from backend. |
| Missing audit events | Decisions cannot be reconstructed | Service-level audit requirement for contracts, rates, outcomes, recalculation, comparisons, recommendations and memberships. |
| Invalid outcome transitions | Success and reversal history becomes unreliable | Central outcome state machine and append-only outcome API. |
| Low sample recommendations | Misleading Scale/Stop decision | Comparison eligibility checks; insufficient evidence always returns Investigate. |
| Mutable historical setup | Old economics change silently | Versioned contracts/rates/configurations and conflict responses for in-use edits. |
| Long analytics requests | Poor demo responsiveness | PostgreSQL aggregates first, bounded date ranges, Redis cache later; background jobs deferred unless measured need appears. |
| Demo reset damages real data | Data loss | Demo dataset marker, environment gate, owner authorization and fail-closed reset validation. |
| Refresh/logout without session persistence | Revoked tokens remain usable | Add hashed `auth_sessions` security table and rotate refresh tokens. |

### Recommended implementation order

1. Authentication, organizations, projects and authorization.
2. Workflows, contracts, providers, rates and configurations.
3. Runs, model calls, tool calls and idempotency.
4. Outcomes, costs and failure waste.
5. Dashboard analytics and configuration comparison.
6. Recommendations, audit retrieval and demo automation.

This order produces testable end-to-end slices rather than dozens of disconnected routes.

---

## 26. Final API Summary

This API design is realistic for a three-month modular-monolith MVP because all endpoints are served by one FastAPI application, one PostgreSQL source of truth and one shared authorization model. Real provider adapters, autonomous routing, cloud billing, distributed ingestion and enterprise chargeback remain outside scope.

The design still preserves industry-grade properties: versioned setup resources, project-level authorization, idempotent telemetry, deterministic calculations, explicit unknown values, append-only outcome history, evidence-linked waste, reproducible comparison cohorts and auditable recommendation rules.

Most importantly, the API supports the central OutcomeIQ proof through a traceable sequence:

1. Start comparable Economy-first and Quality-first workflow runs.
2. Log their model calls, tool calls, retries and fallbacks.
3. Calculate authoritative cost without double counting.
4. Record verified business outcomes separately from technical completion.
5. Compute cost per attempt and cost per successful outcome.
6. Compare both configurations over frozen cohorts.
7. Generate a recommendation linked to numerical evidence.

The resulting API can therefore demonstrate, reproducibly, that **the cheapest workflow per attempt may not be the cheapest workflow per successful business outcome**.
