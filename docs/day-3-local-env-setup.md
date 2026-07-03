# OutcomeIQ — Day 3 Local Environment Setup

This guide configures the local backend environment for PostgreSQL without committing credentials or creating tables.

The exact private file path is:

```text
C:\Users\soham\OneDrive\Documents\pro\backend\.env
```

`backend/.env` is the private local configuration file for this development machine. It is excluded by `.gitignore` and must never be committed.

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

Exact variable format inside `backend/.env`:

```text
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/outcomeiq_dev
```

Replace `your_password` only inside the uncommitted `backend/.env` file.

Do not place the real password in README files, documentation, SQL helpers, source code, screenshots or Git-tracked files.

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

### Test before creating `.env`

If `backend/.env` does not exist, run:

```powershell
.\scripts\check_db_ready.ps1
```

Expected result:

```text
DATABASE NOT CONFIGURED
```

### Test after creating `.env`

After PostgreSQL is running, `outcomeiq_dev` exists and `DATABASE_URL` is set, run the same command:

```powershell
.\scripts\check_db_ready.ps1
```

Expected result:

```text
DATABASE CONNECTED
```

Once the local database and private URL are correct, `DATABASE CONNECTED` is the expected Day 3 setup result.

### Output meanings

| Output | Meaning |
|---|---|
| `DATABASE NOT CONFIGURED` | `.env` is missing or `DATABASE_URL` is empty. This is acceptable in early Day 3. |
| `DATABASE CONNECTED` | SQLAlchemy successfully executed `SELECT 1`. No table was created. |
| `DATABASE ERROR` | A URL is configured but connectivity failed, or the verification script itself could not complete. Review the safe accompanying message. |

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

## 8. Common Connection Errors

### Wrong password

PostgreSQL rejects the login and the check reports `DATABASE ERROR`. Re-enter the local password in `backend/.env`. Do not print or share the URL.

### Database does not exist

Confirm pgAdmin contains a database named exactly `outcomeiq_dev` and that the URL uses the same spelling.

### PostgreSQL service is not running

Start the PostgreSQL Windows service or local server, then rerun the check.

### Port 5432 is blocked or changed

Confirm PostgreSQL is listening on port `5432`. If installation uses another port, update only the local `.env` URL and local firewall configuration.

### `psycopg2` is missing

Activate the project virtual environment and install the existing requirements manually:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

The verification script never installs missing packages automatically.
