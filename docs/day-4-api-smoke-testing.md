# OutcomeIQ — Day 4 Auth/Project API Smoke Testing

## Purpose

The PowerShell smoke test validates the live local API path from registration through project membership. It is intentionally separate from pytest because it requires a running backend and writes synthetic rows to the local development database.

## Prerequisites

- PostgreSQL is running and `scripts/check_db_ready.ps1` reports `DATABASE CONNECTED`.
- Alembic migrations are applied and `scripts/check_db_tables.ps1` reports `ALL CORE TABLES EXIST`.
- Backend dependencies are installed.
- The backend is already running at `http://127.0.0.1:8000`.

Start the backend in the first PowerShell window:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
.\scripts\run_backend.ps1
```

Run the smoke test from a second PowerShell window:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
.\scripts\smoke_auth_project_api.ps1
```

Expected result:

```text
AUTH PROJECT API SMOKE CHECK PASSED
```

## What It Tests

The script uses a timestamp-based `@outcomeiq.local` synthetic email and slugs, then:

1. Checks API health.
2. Registers a synthetic user.
3. Logs in and retains the token only in memory.
4. Calls `/api/v1/auth/me`.
5. Creates an organization.
6. Creates a project.
7. Confirms the project appears in the user's member-scoped list.
8. Confirms the user is the project owner.

The authentication schemas retain `EmailStr` validation for normal addresses and explicitly allow the reserved `@outcomeiq.local` domain for local smoke users. The script sends JSON produced by `ConvertTo-Json` with `ContentType application/json`.

The script never prints the password or access token. If an API request fails, it prints the response body after redacting those sensitive values so FastAPI validation details remain visible. It never starts the backend, creates tables, runs migrations or deletes data.

## Common Failures

- **Backend not running:** Start it with `scripts/run_backend.ps1` in another window.
- **Database not connected:** Run `scripts/check_db_ready.ps1` and verify local PostgreSQL settings.
- **Migrations not applied:** Run `scripts/db_migrate.ps1`, then check tables.
- **Auth endpoint missing:** Restart the backend after installing the latest code/dependencies.
- **Duplicate slug/email:** The script uses millisecond timestamps, so collisions are unlikely. Wait and rerun if local clock reuse causes one.
- **403 project access:** Confirm project creation produced the automatic owner membership.

## Data Warning

Every successful run creates one local test user, organization, project, owner membership and several audit records. The script intentionally does not delete them. Use it only against the local development database—not production or shared environments.
