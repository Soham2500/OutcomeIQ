# OutcomeIQ — First Alembic Infrastructure Migration

## Purpose

Alembic is the database migration tool used with SQLAlchemy. It records reviewed schema changes as versioned Python revisions so development, test and production databases can be moved to the same known schema in a repeatable way.

OutcomeIQ's first revision creates only `system_metadata`. This infrastructure table is intentionally independent of users, projects, workflows and outcomes. It verifies that model registration, migration discovery, PostgreSQL connectivity and upgrade tracking work before business schema work begins.

## Model and Revision

- Model: `app.models.system.SystemMetadata`
- Table: `system_metadata`
- Revision: `0001_system_metadata`
- Migration file: `backend/alembic/versions/20260704_0001_create_system_metadata.py`

The table contains a UUID primary key, a unique non-null metadata key, optional value and description fields, and timezone-aware creation/update timestamps. The revision creates no other table.

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

The local development database has completed this migration:

- Database readiness: `DATABASE CONNECTED`
- Current revision: `0001_system_metadata (head)`
- Table verification: `SYSTEM_METADATA TABLE EXISTS`

Running `db_migrate.ps1` again while the database is already at head should make no schema change.

## Rollback Warning

The revision supports downgrade by dropping `system_metadata`, but no rollback helper script is provided. A downgrade deletes the table and any data stored in it. Review the target revision and preserve required data before manually running any downgrade command.

## Intentionally Not Created

- User, organization, project or authentication tables
- Workflow, run, call, outcome or cost tables
- Business APIs or authentication logic
- Redis or frontend components
- Automatic database creation or automatic migration at application startup

The infrastructure baseline is complete. The next step is to review the smallest tenant-aware business model slice before creating any business table or migration.
