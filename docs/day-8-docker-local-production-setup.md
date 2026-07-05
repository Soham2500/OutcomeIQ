# OutcomeIQ — Day 8 Docker Local Production Setup

## Purpose

The root Docker Compose stack provides a production-like local demonstration environment for OutcomeIQ. It builds immutable backend and frontend images, runs PostgreSQL on an internal Docker network and preserves database state in a named volume.

This setup is for local demonstration only. It is not a production security or cloud-deployment design.

## Services

### PostgreSQL

- Image: `postgres:16-alpine`
- Internal hostname: `postgres`
- Internal port: `5432`
- Named volume: `outcomeiq_postgres_data`
- Health checked with `pg_isready`
- Not published to the host

### Backend

- Python 3.12 slim image
- FastAPI served by Uvicorn on `0.0.0.0:8000`
- Receives database, CORS and local JWT configuration from Compose
- Contains Alembic and explicit pricing-seed tooling
- Waits for PostgreSQL health before startup

### Frontend

- React/Vite application built in a Node multi-stage image
- Static build served by nginx Alpine
- SPA fallback supports `/dashboard`, `/projects`, `/recommendations` and `/demo-guide`
- Browser API base URL is compiled as `http://127.0.0.1:8000/api/v1`

## Local URLs

- Backend: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`
- Frontend: `http://127.0.0.1:8080`

## Full Verification

Start Docker Desktop, then run from the project root:

```powershell
.\scripts\docker_verify.ps1
```

The verifier builds images, starts services, waits for backend health, applies reviewed Alembic migrations, seeds local demo pricing and checks the nginx frontend. It leaves containers and the PostgreSQL volume running for inspection.

A successful run ends with:

```text
DOCKER LOCAL VERIFY PASSED
```

## Individual Commands

```powershell
.\scripts\docker_build.ps1
.\scripts\docker_up.ps1
.\scripts\docker_migrate.ps1
.\scripts\docker_seed_pricing.ps1
.\scripts\docker_logs.ps1
.\scripts\docker_backend_shell.ps1
.\scripts\docker_down.ps1
```

`docker_down.ps1` deliberately does not delete volumes. Restarting the stack preserves local database state.

After migration and pricing seed, the existing API demo-data script can populate the containerized application:

```powershell
.\scripts\seed_demo_data_via_api.ps1
```

## Environment and Security

`backend/.env` and `frontend/.env` are excluded from Docker contexts and Git. The frontend image uses a non-secret build argument for its public API base URL.

The credentials and signing key written directly in `docker-compose.yml` are obvious local demo placeholders only. Change them before any shared or production deployment. A production design should inject secrets through a managed secret store rather than source control.

## Existing Non-Docker Workflow

The original commands remain valid and unchanged:

```powershell
.\scripts\run_backend.ps1
.\scripts\run_frontend.ps1
.\scripts\db_migrate.ps1
.\scripts\db_seed_pricing.ps1
```

They continue to use the private local backend environment and host PostgreSQL configuration.

## Intentionally Not Implemented

- Cloud deployment
- HTTPS or reverse-proxy TLS termination
- Production secret manager
- Container orchestration or autoscaling
- Real AI-provider calls
- Real cloud/provider billing integration
