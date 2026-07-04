# OutcomeIQ

OutcomeIQ is an outcome-aware AI FinOps platform that connects the complete cost of AI workflows to verified business outcomes. Its initial customer-support MVP is designed to prove that the cheapest workflow per attempt may not be the cheapest workflow per successful outcome.

**GitHub:** [Soham2500/OutcomeIQ](https://github.com/Soham2500/OutcomeIQ)

## Current Development Status

- **Day 1 planning:** Complete
- **Day 2 backend foundation and closure:** 100% complete
- **FastAPI application:** Running successfully
- **Swagger UI:** Working
- **Automated tests:** 19 foundation, authentication and API-contract tests passing
- **Smoke API check:** Root, health and readiness passing
- **Day 3 database foundation:** 100% complete; ready for Day 4
- **PostgreSQL:** Local `outcomeiq_dev` connection verified
- **Database migrations/tables:** `0002_core_identity_projects` applied; all core tables exist
- **Data access layer:** Core Pydantic schemas and SQLAlchemy repositories added
- **Development seed:** Verified one safe demo row per core table
- **Authentication:** Basic register, login, bearer JWT and current-user foundation implemented
- **Organization/project APIs:** Authenticated CRUD foundation implemented with audit events
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
│   ├── alembic/                Migration environment and first infrastructure revision
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

## Day 2 documentation

- [Backend foundation progress](docs/day-2-backend-foundation.md)
- [Day 2 checkpoint](docs/day-2-checkpoint.md)
- [Day 2 final summary](docs/day-2-final-summary.md)
- [GitHub setup guide](docs/github-setup.md)
- [Day 3 database setup plan](docs/day-3-database-setup-plan.md)
- [Day 3 local environment setup](docs/day-3-local-env-setup.md)
- [Safe Day 3 `.env` template](docs/day-3-env-template.md)
- [Local PostgreSQL setup](docs/postgresql-local-setup.md)
- [Day 3 checkpoint](docs/day-3-checkpoint.md)
- [First Alembic infrastructure migration](docs/day-3-alembic-migration.md)
- [Core identity and project models](docs/day-3-core-database-models.md)
- [Core data access layer](docs/day-3-core-data-access-layer.md)
- [Day 3 final summary](docs/day-3-final-summary.md)
- [Day 4 authentication readiness](docs/day-4-auth-readiness.md)
- [Day 4 starter prompt](docs/day-4-start-prompt.md)
- [Day 4 authentication testing](docs/day-4-auth-testing.md)
- [Day 4 checkpoint](docs/day-4-checkpoint.md)
- [Organization and project API guide](docs/day-4-organization-project-apis.md)
- [Manual API testing sequence](docs/day-4-manual-api-testing.md)

## Backend foundation status

The Day 2 foundation includes:

- FastAPI application metadata and lifecycle logging
- `/api/v1` router
- Configurable CORS origins
- Environment-based application settings
- Structured JSON console logging
- Conditional SQLAlchemy engine/session foundation with no import-time connection
- Safe database `SELECT 1` readiness helper
- Alembic metadata registered with infrastructure and core identity/project models
- Applied infrastructure and core identity/project migrations
- Core Pydantic schemas, repositories and explicit development seed tooling
- Root, health and readiness routes
- Three endpoint tests, two model tests and four access/diagnostic import tests
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
.\scripts\check_db_ready.ps1
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\db_seed_dev.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
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
19 passed
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
| POST | `/api/v1/auth/register` | Register a user with a securely hashed password |
| POST | `/api/v1/auth/login` | Return a bearer JWT for valid credentials |
| GET | `/api/v1/auth/me` | Return the current authenticated user |
| POST/GET | `/api/v1/organizations` | Create or list organizations |
| GET/PATCH | `/api/v1/organizations/{organization_id}` | Read or update an organization |
| POST/GET | `/api/v1/projects` | Create or list projects |
| GET/PATCH | `/api/v1/projects/{project_id}` | Read or update a project |
| GET | `/api/v1/projects/{project_id}/members` | List project memberships |
| GET | `/docs` | Swagger UI |

The readiness endpoint reports PostgreSQL as `not_configured`, `connected` or `error`. Redis remains `not_configured`. A missing database never prevents FastAPI startup.

## Day 3 database foundation complete

Create the local environment file manually if needed:

```powershell
Copy-Item backend\.env.example backend\.env
```

Edit only the private `backend\.env` file and use this format:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `YOUR_PASSWORD` locally and never commit the file. Before PostgreSQL or `.env` setup, the expected diagnostic output is `DATABASE NOT CONFIGURED`.

Check database readiness without starting FastAPI:

```powershell
.\scripts\check_db_ready.ps1
```

After PostgreSQL, `outcomeiq_dev` and the private URL are configured, the expected output is `DATABASE CONNECTED`. `DATABASE ERROR` means the configured connection could not be verified; the script does not expose the URL.

Alembic and table checks are available through project-root helper scripts:

```powershell
.\scripts\db_history.ps1
.\scripts\db_current.ps1
.\scripts\db_migrate.ps1
.\scripts\check_db_tables.ps1
.\scripts\check_core_data.ps1
.\scripts\inspect_db_schema.ps1
.\scripts\validate_alembic_state.ps1
```

`db_migrate.ps1` is the only command above that changes database schema. It applies reviewed pending revisions through Alembic. The other scripts inspect connectivity, revision state or table existence.

Both reviewed migrations are applied. The table checker reports `ALL CORE TABLES EXIST`, Alembic validation reports `ALEMBIC STATE VALID`, and the safe seed exists once in each core table. No workflow, cost or outcome table exists.

## Test authentication in Swagger

Start the backend, open `http://127.0.0.1:8000/docs`, register a synthetic user, log in, copy the returned access token, select **Authorize**, paste the token into the HTTP Bearer field, and call `GET /api/v1/auth/me`.

Never use real credentials in development or commit `backend/.env`. See [Day 4 authentication testing](docs/day-4-auth-testing.md) for the complete walkthrough.

## Next development steps

### Day 4 authenticated organization/project APIs

- Password hashing, auth schemas/service and bearer JWT utilities are implemented
- Register, login and current-user endpoints are available
- Test manually through Swagger using `docs/day-4-auth-testing.md`
- Organization/project create, list, read and update endpoints are available
- Project creators are automatically added as owners
- Creates and updates append safe audit events
- Next, enforce membership and role-based authorization

Never commit `backend/.env`, hardcode JWT secrets or expose `hashed_password`. Current organization/project access requires authentication but does not yet enforce tenant membership or RBAC. Workflow APIs and frontend work remain separate milestones.
