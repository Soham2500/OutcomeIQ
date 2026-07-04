# OutcomeIQ — Day 3 Core Database Models

## Purpose

This batch establishes the minimum identity, tenancy and project ownership structure needed before authentication and project APIs are implemented. These tables come first because every later workflow, cost and outcome record must eventually belong to a controlled project boundary and be attributable to a user or system action.

The batch deliberately defines persistence only. It does not implement login, authorization, API routes or business workflows.

## Table Summary

| Table | Purpose |
|---|---|
| `users` | Stores future application identities. The password hash remains nullable until authentication is designed. |
| `organizations` | Defines the top-level tenant and ownership boundary. |
| `projects` | Defines the primary operational and future authorization boundary within an organization. |
| `project_members` | Associates users with projects and records a future authorization role. |
| `audit_events` | Provides a redaction-safe foundation for significant user or system activity. |

The existing `system_metadata` table remains the infrastructure baseline and is not modified by this batch.

## Relationship Summary

```text
organizations 1 ──< projects 1 ──< project_members >── 1 users
       │                 │                                  │
       └───────────────< audit_events >─────────────────────┘
```

- Every project belongs to one organization.
- A project membership links one user to one project.
- `(organization_id, slug)` uniquely identifies a project within its organization.
- `(project_id, user_id)` permits only one membership per user and project.
- Audit events may reference a user, organization and project, but those references are nullable for future system-level events.
- Foreign-key deletion is restricted so historical and ownership references are not silently removed.

## Status and Role Values

Python string enums define the currently approved values:

- User: `active`, `inactive`, `suspended`
- Organization: `active`, `inactive`
- Project: `active`, `archived`
- Project member: `owner`, `admin`, `member`, `viewer`
- Audit action: `create`, `update`, `delete`, `login`, `logout`, `system`

Database columns remain simple strings in this migration. Service-layer validation and transition rules are deferred until the corresponding use cases are implemented.

## Migration

The prepared revision is:

```text
backend/alembic/versions/20260704_0002_create_core_identity_project_tables.py
```

It creates only `users`, `organizations`, `projects`, `project_members` and `audit_events`. Its downgrade removes them in reverse foreign-key dependency order. Downgrade is destructive and must not be run against development data without review and backup.

From the project root, inspect and apply pending migrations deliberately:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
```

Verify the approved table set afterward:

```powershell
.\scripts\check_db_tables.ps1
```

Expected post-migration result:

```text
ALL CORE TABLES EXIST
```

## Intentionally Not Created

- Login, registration, password hashing, JWT or authorization logic
- Authentication or project API endpoints
- Organization-level membership tables or services
- Workflow, model-call or tool-call tables
- Outcome, cost, waste, comparison or recommendation tables
- Redis jobs, analytics pipelines or frontend code

## Next Step

Revision `0002_core_identity_projects` is applied, Alembic is at head, all six approved tables exist, and the seed is verified. The next step is reviewing Day 4 authentication boundaries.
