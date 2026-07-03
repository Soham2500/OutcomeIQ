# OutcomeIQ — Day 3 Local Environment Setup

This guide configures the local backend environment for PostgreSQL without committing credentials or creating tables.

## 1. Create `backend/.env` Manually

From the project root in Windows PowerShell:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
```

If `backend\.env` does not already exist, copy the safe example:

```powershell
Copy-Item backend\.env.example backend\.env
```

If the file already exists, do not overwrite it. Open it in a text editor and update only the required local values.

## 2. Understand `DATABASE_URL`

`DATABASE_URL` tells SQLAlchemy:

- Which PostgreSQL driver to use
- Which user should connect
- The database password
- The PostgreSQL host and port
- The database name

Example format:

```text
postgresql+psycopg2://postgres:your_password@localhost:5432/outcomeiq_dev
```

Replace `your_password` only inside the uncommitted `backend/.env` file.

If the password contains reserved URL characters such as `@`, `:`, `/`, `#` or `%`, URL-encode it or use a password without those characters for local development. Never print the final URL in logs or screenshots.

## 3. Safe `backend/.env` State Before PostgreSQL Exists

The backend may continue to use:

```text
DATABASE_URL=
```

With an empty value:

- FastAPI still starts.
- `/api/v1/health` remains unchanged.
- `/api/v1/ready` returns `database=not_configured`.
- Tests do not require PostgreSQL.

## 4. Do Not Commit `.env`

`backend/.env` may contain credentials and must never be committed.

Verify the ignore rule from the project root:

```powershell
git check-ignore -v backend\.env
```

Expected behavior: Git prints the `.gitignore` rule that excludes `.env`.

Confirm the safe example remains trackable:

```powershell
git check-ignore backend\.env.example
```

Expected behavior: no ignore rule is printed for `.env.example`.

## 5. Check Database Readiness Without Starting the API

From the project root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_db_ready.ps1
```

Possible results:

- `DATABASE NOT CONFIGURED`
- `DATABASE CONNECTED`
- `DATABASE ERROR`

The script never installs packages, creates databases, creates tables or runs migrations.

## 6. Check Readiness Through the API

Before PostgreSQL configuration, start the API:

```powershell
.\scripts\run_backend.ps1
```

In another PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/ready
```

Expected database state:

```text
not_configured
```

After creating PostgreSQL and setting `DATABASE_URL`, restart Uvicorn so cached settings and the SQLAlchemy engine are rebuilt. Run the same readiness request again.

Expected database state when the credentials and database are correct:

```text
connected
```

If the state is `error`, verify the database service, host, port, database name, user, password and firewall. The API intentionally returns a safe generic error and does not expose the connection URL.

## 7. Alembic Environment Behavior

Alembic reads the same `DATABASE_URL` through application settings. With no URL configured, Alembic stops with a clear error.

No migration exists yet. Do not run upgrade commands until a reviewed migration has been created in a later step.
