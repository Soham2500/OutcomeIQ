# OutcomeIQ Backend

Initial FastAPI modular-monolith foundation for the OutcomeIQ outcome-aware AI FinOps platform.

## Current status

Available now:

- FastAPI application setup
- Versioned API router
- Root, health and readiness endpoints
- Environment-backed settings
- Configurable CORS origins
- Structured JSON logging
- A non-connecting database-session placeholder
- Basic endpoint tests
- Docker packaging

Not implemented yet:

- Authentication
- Business APIs
- PostgreSQL connection
- SQLAlchemy models
- Database tables
- Alembic migrations
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
```

- `check_backend.ps1` verifies the expected structure without changing anything.
- `test_backend.ps1` activates `.venv` and runs pytest.
- `day2_verify.ps1` checks all Day 1/2 deliverables and runs tests.
- `run_backend.ps1` activates `.venv` and starts Uvicorn with auto-reload.
- `smoke_api.ps1` checks the three running API endpoints from another terminal.
- `check_docker.ps1` reports Docker and Compose availability without starting anything.

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

No PostgreSQL or Redis URL is required at this stage.

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
| GET | `/api/v1/ready` | Dependency readiness; database and Redis are not configured |
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
3 passed
```

Run only the health tests when needed:

```powershell
python -m pytest tests\test_health.py -v
```

The pytest configuration intentionally leaves warnings visible.

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

Remaining backend-foundation work should add shared response/error schemas, request-correlation middleware and exception handling. PostgreSQL session setup, SQLAlchemy models and Alembic migrations remain Day 3 work and must follow the approved database design.
