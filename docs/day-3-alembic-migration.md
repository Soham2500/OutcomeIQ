# OutcomeIQ — Alembic Migration Foundation

## Purpose

Alembic is the database migration tool used with SQLAlchemy. It records reviewed schema changes as versioned Python revisions so development, test and production databases can be moved to the same known schema in a repeatable way.

OutcomeIQ's first revision creates only `system_metadata`. The second prepared revision adds the minimum identity, tenancy, project-membership and audit foundation. Workflow economics remains outside this migration batch.

## Model and Revision

- Model: `app.models.system.SystemMetadata`
- Table: `system_metadata`
- Revision: `0001_system_metadata`
- Migration file: `backend/alembic/versions/20260704_0001_create_system_metadata.py`

The table contains a UUID primary key, a unique non-null metadata key, optional value and description fields, and timezone-aware creation/update timestamps. The revision creates no other table.

The next ordered revision is:

- Revision: `0002_core_identity_projects`
- Parent: `0001_system_metadata`
- Migration file: `backend/alembic/versions/20260704_0002_create_core_identity_project_tables.py`
- Tables: `users`, `organizations`, `projects`, `project_members`, `audit_events`

## Safe Command Sequence

Run all helper scripts from the project root. First confirm PostgreSQL connectivity:

```powershell
.\scripts\check_db_ready.ps1
```

Inspect migration history and the current database revision:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
```

Apply the reviewed revision only when ready:

```powershell
.\scripts\db_migrate.ps1
```

Verify the table after the upgrade:

```powershell
.\scripts\check_db_tables.ps1
```

Expected post-migration output:

```text
SYSTEM_METADATA TABLE EXISTS
```

Before the initial upgrade, `SYSTEM_METADATA TABLE MISSING` was expected.

## Verified Local Status

The local development database has completed the infrastructure migration:

- Database readiness: `DATABASE CONNECTED`
- Current revision: `0002_core_identity_projects (head)`
- Table verification: `ALL CORE TABLES EXIST`

The database is at head. Running `db_migrate.ps1` again should make no schema change.

## Rollback Warning

The revision supports downgrade by dropping `system_metadata`, but no rollback helper script is provided. A downgrade deletes the table and any data stored in it. Review the target revision and preserve required data before manually running any downgrade command.

## Intentionally Not Created

- Authentication services, authorization rules or API endpoints
- Workflow, run, call, outcome or cost tables
- Business APIs or authentication logic
- Redis or frontend components
- Automatic database creation or automatic migration at application startup

The infrastructure and core migrations are complete. The next step is explicit local seed verification, while authentication and workflow schema work remain deferred.
