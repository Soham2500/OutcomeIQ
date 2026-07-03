# OutcomeIQ — Local PostgreSQL Setup on Windows

This guide prepares a development PostgreSQL database for OutcomeIQ. It does not create application tables; Alembic will manage tables later after model and migration review.

## Prerequisites

Choose one PostgreSQL environment:

- A local Windows PostgreSQL installation with pgAdmin and `psql`
- A future Docker-based PostgreSQL service after Docker Desktop is available
- A separate Supabase development project when local PostgreSQL is impractical

The instructions below assume local PostgreSQL on Windows.

## 1. Start PostgreSQL

Confirm the PostgreSQL Windows service is running. Then open either:

- **pgAdmin** for a graphical workflow, or
- **SQL Shell (`psql`)** for a command-line workflow

Use the administrative credentials chosen during PostgreSQL installation. Keep the password private.

## 2. Create the Development Database in pgAdmin

1. Expand the local PostgreSQL server.
2. Right-click **Databases**.
3. Select **Create → Database**.
4. Set the database name to `outcomeiq_dev`.
5. Use the existing `postgres` owner for initial local setup, or select a dedicated application role if one has already been created.
6. Save the database.

Do not create tables manually in pgAdmin.

## 3. Create the Development Database with `psql`

If using `psql`, connect to the local server as an administrator and create a database named `outcomeiq_dev` through PostgreSQL’s normal database-creation command.

For the first connectivity check, the existing local `postgres` user may be used. A dedicated non-superuser application role should be created before broader development or shared deployment.

Do not execute table-creation statements.

## 4. Application User Guidance

For a simple local bootstrap, using the existing `postgres` user is acceptable temporarily. The safer next step is a dedicated role such as `outcomeiq_app` with access only to `outcomeiq_dev`.

Do not:

- Store the password in source files
- Add the password to `alembic.ini`
- Commit the password to Git
- Reuse production credentials
- Give an application role unnecessary superuser privileges

## 5. Update `backend/.env`

Open:

```text
C:\Users\soham\OneDrive\Documents\pro\backend\.env
```

Set `DATABASE_URL` using the local username, password, host, port and database name.

Example format only:

```text
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/outcomeiq_dev
```

Do not copy the real password into documentation or chat messages.

## 6. Verify Without Creating Tables

From the project root, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_db_ready.ps1
```

Expected result:

```text
DATABASE CONNECTED
```

This performs only `SELECT 1`. It does not create a table or run a migration.

## 7. Verify Through FastAPI Readiness

Restart the backend after changing `.env`:

```powershell
.\scripts\run_backend.ps1
```

In a second PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/ready
```

Expected response fields include:

```text
status   = ready
database = connected
redis    = not_configured
```

If the database is missing, the API still starts and reports `not_configured`. Incorrect configured credentials report `error` without exposing the password or full URL.

## 8. Table and Migration Rule

Do not create OutcomeIQ tables manually.

- SQLAlchemy models will be added incrementally in a later prompt.
- Alembic migrations will be generated only after model review.
- Every migration must be reviewed before upgrade.
- No migration file exists at the end of Day 3 Prompt 1.
- FastAPI startup must never call `Base.metadata.create_all()`.

## 9. Optional Test Database Later

Before integration or downgrade tests, create a separate disposable database such as `outcomeiq_test`. Never run destructive migration tests against `outcomeiq_dev` or a production database.
