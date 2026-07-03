# OutcomeIQ — Local PostgreSQL Setup on Windows

This guide prepares a development PostgreSQL database for OutcomeIQ. It does not create application tables; Alembic will manage tables later after model and migration review.

## Prerequisites

Choose one PostgreSQL environment:

- A local Windows PostgreSQL installation with pgAdmin and `psql`
- A future Docker-based PostgreSQL service after Docker Desktop is available
- A separate Supabase development project when local PostgreSQL is impractical

The instructions below assume local PostgreSQL on Windows.

## SQL Helper File

The repository contains a password-free helper at:

```text
database/local/create_outcomeiq_dev.sql
```

Its only statement creates the empty `outcomeiq_dev` database. It does not create schemas, tables, users or application data and is safe to commit.

To use it manually, open the file in pgAdmin’s Query Tool while connected to an existing administrative database such as `postgres`, then execute it once. Do not run it again after `outcomeiq_dev` exists.

The PostgreSQL password must remain only in the ignored local `backend/.env` file. Never place the password in this SQL helper, documentation or Git-tracked configuration, and never commit `backend/.env`.

## Manual Steps for Soham Using pgAdmin

1. Open **pgAdmin**.
2. Log in using the PostgreSQL master password selected during installation.
3. Expand **Servers** and then the local PostgreSQL server.
4. Right-click **Databases**.
5. Select **Create → Database**, name it `outcomeiq_dev` and save it.
6. Do not create tables manually.
7. Open the folder `C:\Users\soham\OneDrive\Documents\pro\backend`.
8. Create a private file named `.env` by copying `.env.example` if necessary.
9. Set `DATABASE_URL` with the correct local PostgreSQL password.
10. Return to the project root and run `.\scripts\check_db_ready.ps1`.
11. Start the backend with `.\scripts\run_backend.ps1`.
12. Open `http://127.0.0.1:8000/api/v1/ready` and confirm `database` is `connected`.

These steps create only the empty development database. OutcomeIQ tables will be created later through reviewed Alembic migrations.

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

If the PostgreSQL `createdb` utility is available on `PATH`, the beginner-safe alternative is:

```powershell
createdb -U postgres outcomeiq_dev
```

The command prompts for credentials according to the local PostgreSQL configuration. Do not put the password directly in the command.

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
