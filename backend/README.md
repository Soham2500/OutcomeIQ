# OutcomeIQ Backend

Initial FastAPI modular-monolith foundation for the OutcomeIQ outcome-aware AI FinOps platform.

## Current status

**Day 2 is complete.** Day 3 now has verified PostgreSQL connectivity and a prepared first infrastructure migration. It has not been applied automatically.

Available now:

- FastAPI application setup
- Versioned API router
- Root, health and readiness endpoints
- Environment-backed settings
- Configurable CORS origins
- Structured JSON logging
- SQLAlchemy declarative base with no business models
- Conditional engine and session factory when `DATABASE_URL` is present
- Safe database readiness check using `SELECT 1`
- Alembic environment with the `SystemMetadata` model registered
- First infrastructure migration for `system_metadata`
- Endpoint and model-metadata tests
- Docker packaging

Not implemented yet:

- Authentication
- Business APIs
- Business SQLAlchemy models and tables
- Applied migration state (until `db_migrate.ps1` is run deliberately)
- Redis integration
- Frontend code

## Prerequisites

- Python 3.11 or newer; Python 3.12 is recommended
- `pip`
- Docker Desktop only if using Docker

## Developer scripts

The repository provides PowerShell helpers. Run them from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_backend.ps1
.\scripts\test_backend.ps1
.\scripts\day2_verify.ps1
.\scripts\run_backend.ps1
.\scripts\smoke_api.ps1
.\scripts\check_docker.ps1
.\scripts\check_db_ready.ps1
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

- `check_backend.ps1` verifies the expected structure without changing anything.
- `test_backend.ps1` activates `.venv` and runs pytest.
- `day2_verify.ps1` checks all Day 1/2 deliverables and runs tests.
- `run_backend.ps1` activates `.venv` and starts Uvicorn with auto-reload.
- `smoke_api.ps1` checks the three running API endpoints from another terminal.
- `check_docker.ps1` reports Docker and Compose availability without starting anything.
- `check_db_ready.ps1` reports database configuration/connectivity without creating databases, tables or migrations.
- `db_history.ps1` and `db_current.ps1` inspect Alembic state.
- `db_migrate.ps1` explicitly applies reviewed migrations through `alembic upgrade head`.
- `check_db_tables.ps1` safely checks whether `system_metadata` exists.

## Setup on Windows PowerShell

Open PowerShell and begin at the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
```

Create the root virtual environment:

```powershell
python -m venv .venv
```

Allow activation scripts for the current PowerShell process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

Move into the backend directory:

```powershell
cd backend
```

Create a local environment file if one does not already exist:

```powershell
Copy-Item .env.example .env
```

No PostgreSQL or Redis URL is required for FastAPI startup. An empty `DATABASE_URL` reports `not_configured`.

## Run the FastAPI server

From the `backend` directory with the virtual environment active:

```powershell
uvicorn app.main:app --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Health: `http://127.0.0.1:8000/api/v1/health`
- Readiness: `http://127.0.0.1:8000/api/v1/ready`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Available endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Basic service discovery |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Dependency readiness; database is `not_configured`, `connected` or `error` |
| GET | `/docs` | Swagger UI |

## Stop the server

Press `Ctrl+C` in the PowerShell window running Uvicorn.

## Run the smoke API check

Keep Uvicorn running in the first PowerShell window. Open a second PowerShell window and run from the project root:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\smoke_api.ps1
```

The smoke script reports a helpful failure if the API is not running; it never launches Uvicorn itself.

## Run tests

From the `backend` directory:

```powershell
python -m pytest -v
```

Expected result:

```text
4 passed
```

Run only the health tests when needed:

```powershell
python -m pytest tests\test_health.py -v
```

The pytest configuration intentionally leaves warnings visible.

The current `StarletteDeprecationWarning` related to FastAPI TestClient and HTTPX is non-blocking. It does not change the `4 passed` result and should remain visible until the upstream compatibility path is addressed deliberately.

## Verified commands

From the project root:

```powershell
.\scripts\day2_verify.ps1
.\scripts\test_backend.ps1
.\scripts\run_backend.ps1
```

With the API running in the first window, use a second PowerShell window:

```powershell
.\scripts\smoke_api.ps1
```

Verified results are four passing pytest tests and successful root, health and readiness smoke checks.

## Run with Docker

Docker Desktop must be installed and running.

From the `backend` directory:

```powershell
docker compose up --build
```

Check the health endpoint:

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/health
```

Stop and remove the backend container:

```powershell
docker compose down
```

The Compose file intentionally contains only the backend service. PostgreSQL and Redis are deferred.

## Configuration

Settings load from environment variables or `backend\.env`. Available values are documented in `.env.example`.

Current optional placeholders:

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`

Do not use the example JWT secret in a deployed environment.

## Database foundation

Create `backend\.env` manually from the safe example if needed:

```powershell
Copy-Item .env.example .env
```

Set the private local value using this format:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `YOUR_PASSWORD` locally. Never commit or print the completed URL.

From the project root, check status with:

```powershell
.\scripts\check_db_ready.ps1
```

The result is one of:

- `DATABASE NOT CONFIGURED` before `.env`/URL setup; acceptable in early Day 3
- `DATABASE CONNECTED` after PostgreSQL and credentials are correct
- `DATABASE ERROR` when configured connectivity fails or the script cannot complete

The check performs only `SELECT 1`. It never creates a database, table or migration.

## First Alembic infrastructure migration

Alembic uses the private `DATABASE_URL` from application settings and `Base.metadata` from `app/db/base.py`. Only `SystemMetadata` is registered for this milestone.

From the project root, inspect migration state with:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
```

Apply the reviewed migration explicitly, then verify the table:

```powershell
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
```

The prepared revision creates only `system_metadata`. It does not create business tables. See `docs/day-3-alembic-migration.md` for the command sequence and rollback warning.

## Troubleshooting

### PowerShell blocks virtual-environment activation

Run this in the same PowerShell window, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run these commands from the project root. If already inside `backend`, return to the root first with `cd ..`.

### `python` is not recognized

Try the Windows Python launcher:

```powershell
py -m venv .venv
```

If neither `python` nor `py` works, reinstall Python and select **Add Python to PATH**.

### `ModuleNotFoundError: app`

Confirm Uvicorn and pytest are running from:

```text
C:\Users\soham\OneDrive\Documents\pro\backend
```

Also confirm the root virtual environment is active.

### `ModuleNotFoundError: fastapi`

Activate the virtual environment and reinstall dependencies from the project root:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### Port 8000 is already in use

Use a different port:

```powershell
uvicorn app.main:app --reload --port 8001
```

### Swagger UI does not open

Confirm Uvicorn shows a successful startup and open `http://127.0.0.1:8000/docs`, not the filesystem path.

### Docker cannot start

Confirm Docker Desktop is running and configured for Linux containers.

## Next steps

The next database step is to apply and verify the first infrastructure migration deliberately. Business SQLAlchemy models, tables and APIs remain deliberately unimplemented and must follow the approved database design.
