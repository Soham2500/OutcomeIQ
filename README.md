# OutcomeIQ

OutcomeIQ is an outcome-aware AI FinOps platform that connects the complete cost of AI workflows to verified business outcomes. Its initial customer-support MVP is designed to prove that the cheapest workflow per attempt may not be the cheapest workflow per successful outcome.

**GitHub:** [Soham2500/OutcomeIQ](https://github.com/Soham2500/OutcomeIQ)

## Current Development Status

- **Day 1 planning:** Complete
- **Day 2 backend foundation:** Complete
- **FastAPI application:** Running successfully
- **Swagger UI:** Working
- **Automated tests:** 3 health/foundation tests passing
- **PostgreSQL:** Not configured yet
- **Authentication:** Not implemented yet
- **Frontend:** Not implemented yet

The project currently provides a clean FastAPI modular-monolith foundation with environment-backed settings, structured logging, versioned routing, health/readiness endpoints, tests and Docker packaging.

## Technology stack

| Area | Technology |
|---|---|
| Backend | FastAPI, Python |
| Validation/settings | Pydantic, pydantic-settings |
| Planned persistence | PostgreSQL, SQLAlchemy, Alembic |
| Planned cache/jobs | Redis |
| Analytics | Pandas, Scikit-learn |
| Frontend | React, Tailwind CSS, Recharts |
| Packaging | Docker, Docker Compose |
| Testing | Pytest, HTTPX/FastAPI TestClient |

## Repository structure

```text
pro/
├── backend/                    FastAPI modular-monolith backend
│   ├── app/                    Application source
│   ├── tests/                  Backend tests
│   ├── scripts/                Future administrative scripts
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── docs/                       Product and engineering documentation
├── scripts/                    PowerShell development and verification helpers
├── .gitignore
└── README.md
```

## Completed planning documents

The Day 1 planning package contains:

- [Product understanding](docs/product-understanding.md)
- [Three-month MVP scope](docs/mvp-scope.md)
- [System architecture](docs/system-architecture.md)
- [Database design](docs/database-design.md)
- [REST API design](docs/api-design.md)
- [GitHub setup guide](docs/github-setup.md)
- [Day 2 checkpoint](docs/day-2-checkpoint.md)

These documents define the architecture and product rules that implementation must follow.

## Backend foundation status

The Day 2 foundation includes:

- FastAPI application metadata and lifecycle logging
- `/api/v1` router
- Configurable CORS origins
- Environment-based application settings
- Structured JSON console logging
- Placeholder database-session module with no connection
- Root, health and readiness routes
- Three endpoint tests
- Backend-only Docker configuration

See [Day 2 backend progress](docs/day-2-backend-foundation.md) and the [backend README](backend/README.md) for details.

## Development scripts

From the project root, PowerShell helpers are available for common tasks:

```powershell
.\scripts\check_backend.ps1
.\scripts\test_backend.ps1
.\scripts\day2_verify.ps1
.\scripts\run_backend.ps1
.\scripts\smoke_api.ps1
.\scripts\check_docker.ps1
```

The check and verification scripts do not install packages, create databases or start Uvicorn. `run_backend.ps1` starts the server only when explicitly invoked. The smoke script expects an already-running API.

## Run the backend locally

Open Windows PowerShell and run:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Swagger UI will be available at:

```text
http://127.0.0.1:8000/docs
```

Stop the server with `Ctrl+C`.

## Run tests

From the `backend` directory with the root virtual environment activated:

```powershell
python -m pytest -v
```

Expected result:

```text
3 passed
```

The existing Starlette/HTTPX compatibility warning may remain visible; pytest is not configured to hide real warnings.

## Run the full Day 2 verification

From the project root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\day2_verify.ps1
```

The script checks required documentation, backend files, root files and the virtual environment, then runs the backend tests. A successful run ends with:

```text
DAY 2 CHECK PASSED
```

## Smoke API check

Start the API in one PowerShell window:

```powershell
.\scripts\run_backend.ps1
```

From a second PowerShell window at the project root, run:

```powershell
.\scripts\smoke_api.ps1
```

The script calls `/`, `/api/v1/health` and `/api/v1/ready`. It never starts the server automatically.

## Docker availability check

Check for the Docker CLI and Docker Compose plugin without building or starting anything:

```powershell
.\scripts\check_docker.ps1
```

## Repository formatting files

- `.gitattributes` normalizes source, documentation and PowerShell scripts to LF for consistent cross-platform Git behavior.
- `.editorconfig` standardizes UTF-8, final newlines, trailing whitespace and indentation.

After introducing `.gitattributes`, future Git operations may report normalized line-ending changes once. Review the diff before committing.

## Available endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Basic service discovery |
| GET | `/api/v1/health` | Process liveness |
| GET | `/api/v1/ready` | Current dependency readiness |
| GET | `/docs` | Swagger UI |

The readiness endpoint intentionally reports PostgreSQL and Redis as `not_configured`.

## Next development steps

### Remaining Day 2 hardening

- Add shared response and error schemas
- Add request-correlation middleware
- Add central exception handling
- Add focused tests for configuration and error behavior

### Day 3 database foundation

- Configure PostgreSQL connection settings
- Add SQLAlchemy declarative base and session factory
- Initialize Alembic configuration
- Test connection lifecycle separately
- Introduce domain models only after reviewing the database design sequence

Authentication and frontend implementation remain later milestones.
