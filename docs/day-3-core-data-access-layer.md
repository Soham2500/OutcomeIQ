# OutcomeIQ — Day 3 Core Data Access Layer

## Purpose

This milestone adds a small, explicit database access layer above the applied core schema. It prepares OutcomeIQ for future services and APIs without coupling route handlers directly to SQLAlchemy queries.

## Pydantic Schemas

Schemas define validated input and output shapes independently of database models. The new schema modules cover users, organizations, projects, project memberships and audit events.

Read schemas use Pydantic v2 `from_attributes=True`, allowing future services to serialize SQLAlchemy objects safely. `UserCreate` and `UserRead` intentionally expose neither raw passwords nor `hashed_password`.

## Repositories

Repositories contain focused SQLAlchemy `Session` operations:

- Find, create and list users
- Find, create and list organizations
- Find, create and list projects
- Add and list project members
- Create and list audit events

Create functions explicitly add, commit and refresh records. Repositories currently contain no authentication, permission or tenant-enforcement decisions; those belong in reviewed service-layer use cases.

## Why APIs Are Deferred

Exposing routes before authentication and authorization boundaries are defined would make project data easy to access incorrectly. This milestone verifies persistence contracts first. Login, registration, JWT, permission checks and HTTP endpoints remain separate work.

## Development Seed Data

The local-only seed creates a deterministic demo user, organization, project, owner membership and one system audit event. It uses no real password and stores no secrets. The service checks for each record before creating it, so repeated runs do not intentionally create duplicates.

The seed does not create tables or run migrations. It has been run explicitly and verified with one safe demo record in each core table.

## Commands

Run these from the project root:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
```

Expected table result after migrations:

```text
ALL CORE TABLES EXIST
```

Expected data result after seeding:

```text
CORE DEVELOPMENT DATA FOUND
```

The check script prints row counts but never creates, updates or deletes data.

## Intentionally Not Implemented

- Password hashing or credential validation
- Login, registration, JWT or authorization logic
- API routes
- Workflow, model-call, tool-call, outcome, cost or recommendation tables
- Business seed data for AI workflows
- Frontend code
- Automatic migration or seeding during application startup

## Next Step

The development seed and idempotence checkpoint are complete. Next, design the Day 4 authentication service boundary before exposing any API.
