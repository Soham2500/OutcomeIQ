# OutcomeIQ — Day 3 Database Setup Plan

**Project:** OutcomeIQ — Outcome-aware AI FinOps Platform  
**Milestone:** PostgreSQL, SQLAlchemy and Alembic foundation  
**Document type:** Plan only; no database implementation is performed here

## Day 3 Objective

Day 3 should establish a safe and testable persistence foundation for the existing FastAPI modular monolith.

The objective is to:

1. Make a development PostgreSQL instance available.
2. Configure the backend connection through environment variables.
3. Introduce a SQLAlchemy declarative base, engine and session lifecycle.
4. Initialize Alembic against the same metadata and settings.
5. Verify connectivity, transaction rollback and migration commands.
6. Prepare the first small model slice for later review.

Day 3 should not create all 29 approved MVP tables in one operation.

## PostgreSQL Setup Goal

The development environment should provide one isolated PostgreSQL database used only for OutcomeIQ development.

Recommended properties:

- A dedicated development database such as `outcomeiq_dev`
- A dedicated non-superuser application role
- A separate test database such as `outcomeiq_test` when integration tests begin
- UTF-8 encoding
- UTC timestamps at the application boundary
- Network access limited to the local machine or approved development host
- No production or personal customer data

The production architecture may later use Supabase PostgreSQL, but Day 3 should first prove standard PostgreSQL compatibility.

## Environment Variables Needed

### Required

- `DATABASE_URL`: SQLAlchemy-compatible PostgreSQL URL for the development database

### Recommended Day 3 additions

- `DATABASE_ECHO=false`: Enables SQL logging only during deliberate debugging
- `DATABASE_POOL_PRE_PING=true`: Validates pooled connections before use
- `DATABASE_POOL_SIZE=5`: Small development pool
- `DATABASE_MAX_OVERFLOW=5`: Bounded temporary overflow
- `DATABASE_CONNECT_TIMEOUT=5`: Prevents long startup hangs

### Test configuration

- `TEST_DATABASE_URL`: Separate PostgreSQL database for integration tests

Secrets belong in `backend/.env` or the local shell environment. Only safe placeholders belong in `.env.example`.

Redis remains optional and unconfigured during this milestone.

## SQLAlchemy Setup Plan

### Step 1: Declarative base

Create one shared SQLAlchemy declarative base in the database package. Every later domain model must inherit from this base so Alembic sees one authoritative metadata collection.

### Step 2: Engine creation

Create the PostgreSQL engine from validated settings. Engine creation should not create tables and should not run `metadata.create_all()`.

Recommended behavior:

- Explicit pool settings
- `pool_pre_ping` for stale-connection handling
- Safe SQL logging controlled by environment
- No credentials in logs
- Clear configuration error when `DATABASE_URL` is absent on database-dependent operations

### Step 3: Session factory

Create one `sessionmaker` with:

- Explicit transaction boundaries
- `autoflush` chosen deliberately
- `expire_on_commit` documented
- No global live session

### Step 4: FastAPI dependency

Replace the current placeholder with a generator dependency that:

1. Creates one session per request.
2. Yields it to the service/repository layer.
3. Rolls back after an exception.
4. Closes the session in all cases.

No endpoint should contain raw engine or connection management.

### Step 5: Connectivity tests

Add focused tests for:

- Valid connection
- Invalid configuration
- Session close behavior
- Transaction rollback
- Readiness behavior when PostgreSQL is available or unavailable

Unit tests that do not need PostgreSQL should remain fast and isolated.

## Alembic Migration Setup Plan

### Initialization

Initialize Alembic inside `backend/` and connect its environment to the same application settings and SQLAlchemy metadata.

### Configuration principles

- Do not place database credentials in `alembic.ini`.
- Read `DATABASE_URL` through the application settings layer.
- Set Alembic `target_metadata` to the shared declarative base metadata.
- Use descriptive migration names.
- Keep upgrade and downgrade paths reviewable.
- Run migrations manually; do not apply them automatically on application import.

### First migration policy

Do not autogenerate the entire 29-table schema on Day 3. The first migration should be created only after the first model slice has been reviewed against `database-design.md`.

Before applying a generated migration:

1. Read the migration file.
2. Confirm table, type, nullability, foreign-key and index choices.
3. Confirm downgrade behavior.
4. Review the generated SQL.
5. Apply only to the development database.
6. Verify upgrade and downgrade in the test database.

## Initial Database Models to Prepare Later

The first domain-model slice should establish tenant identity and ownership before workflow economics.

Recommended order for later model work:

1. `users`
2. `organizations`
3. `organization_members`
4. `projects`
5. `project_members`

After that slice is validated, proceed incrementally:

1. Workflows and workflow versions
2. Outcome Contracts and contract versions
3. Providers, models and rate cards
4. Configurations
5. Runs and execution events
6. Costs, outcomes, waste, comparisons and recommendations

Authentication must not be implemented merely because a `users` persistence model exists.

## What Not to Overbuild on Day 3

- Do not create all 29 tables.
- Do not implement repositories for every domain.
- Do not implement authentication.
- Do not create seed data for the complete product.
- Do not add Redis, Celery or message brokers.
- Do not add read replicas or advanced pooling infrastructure.
- Do not add row-level security before the authorization model is implemented.
- Do not add automatic production migration execution.
- Do not add frontend or business APIs.
- Do not use `Base.metadata.create_all()` as a replacement for migrations.

The Day 3 success condition is a trustworthy database foundation, not visible product functionality.

## Safety Checklist Before Creating Database Tables

- [ ] Confirm the connection points to a development database, not production.
- [ ] Confirm the application role is not a PostgreSQL superuser.
- [ ] Confirm `backend/.env` is ignored by Git.
- [ ] Confirm no secret appears in logs, README files or Alembic configuration.
- [ ] Confirm PostgreSQL version and connection driver compatibility.
- [ ] Confirm UUID, `NUMERIC`, `TIMESTAMPTZ`, JSONB and enum strategy against `database-design.md`.
- [ ] Confirm one shared SQLAlchemy metadata source.
- [ ] Confirm models do not create tables during import.
- [ ] Confirm the first migration is small and manually reviewed.
- [ ] Confirm downgrade behavior in a disposable test database.
- [ ] Confirm transaction rollback tests pass.
- [ ] Confirm existing health tests continue to pass.
- [ ] Confirm readiness reports database state without leaking connection details.
- [ ] Create a backup or use a disposable database before destructive migration testing.

No table should be created until every applicable item is complete.

## Manual PostgreSQL Actions Soham Must Do on Day 3

### 1. Choose a local PostgreSQL environment

Select one approach:

- Install and run PostgreSQL locally on Windows.
- Install Docker Desktop and later use an approved PostgreSQL Compose service.
- Create a separate Supabase development project if local installation is impractical.

Do not point development work at a production database.

### 2. Record connection details securely

Collect:

- Host
- Port
- Database name
- Application username
- Application password
- SSL mode when required

Keep these only in the local password manager and `backend/.env`.

### 3. Create the development database and application role

Using PostgreSQL administration tools:

- Create `outcomeiq_dev` or an equivalently named development database.
- Create a dedicated application role such as `outcomeiq_app`.
- Give the role only the privileges needed on the development database/schema.
- Do not use the PostgreSQL administrator account as the application identity.

### 4. Prepare a test database

Create a separate disposable database such as `outcomeiq_test` before database integration tests or downgrade tests are introduced.

### 5. Set local environment values

Copy `backend/.env.example` to `backend/.env` if needed, then set `DATABASE_URL` with the real local development credentials. Set `TEST_DATABASE_URL` only when the test database is ready.

Never commit either value.

### 6. Verify manual connectivity

Use PostgreSQL’s administration client or provider dashboard to verify that the application role can connect to the intended database and cannot access unrelated databases.

### 7. Approve migration execution explicitly

Review every migration and run it manually against development. Do not configure Uvicorn startup to create tables or apply migrations automatically.

## Day 3 Completion Criteria

Day 3 database setup is complete when:

- PostgreSQL development and test connections are available.
- SQLAlchemy engine/session lifecycle is configured without creating tables implicitly.
- Alembic is initialized and reads application configuration safely.
- Connectivity and rollback tests pass.
- Existing three foundation tests still pass.
- The first model/migration slice is reviewed and ready for a separate implementation step.

This sequencing keeps OutcomeIQ aligned with its approved architecture and prevents a large, fragile schema dump.
