# OutcomeIQ — Safe Day 3 `.env` Template

Create the private local file manually at:

```text
C:\Users\soham\OneDrive\Documents\pro\backend\.env
```

Use this template:

```dotenv
APP_NAME=OutcomeIQ API
APP_VERSION=0.1.0
ENVIRONMENT=development
API_V1_PREFIX=/api/v1
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
REDIS_URL=
JWT_SECRET_KEY=change-this-in-development
```

## Required Manual Change

Replace `YOUR_PASSWORD` with the local PostgreSQL password chosen during installation.

If the password contains reserved URL characters such as `@`, `:`, `/`, `#` or `%`, URL-encode it before placing it in `DATABASE_URL`.

## Privacy Rules

- `backend/.env` is private and must never be committed.
- `backend/.env.example` contains placeholders and is safe to commit.
- Never paste the real `DATABASE_URL` into documentation, screenshots, issues or chat messages.
- Never store production credentials in the development `.env`.

Verify that Git ignores the private file:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
git check-ignore -v backend\.env
```

Expected behavior: Git displays the `.gitignore` rule responsible for ignoring the file.

## Creating the File

If `backend/.env` does not exist:

```powershell
Copy-Item backend\.env.example backend\.env
```

Open the copied file in a text editor, replace only the local placeholders and save it. Do not automate real credential creation.

## Verify the Result

From the project root:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\check_db_ready.ps1
```

Expected result after PostgreSQL and `outcomeiq_dev` are available:

```text
DATABASE CONNECTED
```

This check performs only `SELECT 1`; it does not create tables or run migrations.
