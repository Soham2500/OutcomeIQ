# OutcomeIQ — Day 4 Authentication Testing

## Start the Backend

From the project root, activate the existing environment and install the declared dependencies:

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
uvicorn app.main:app --reload
```

Open Swagger UI at `http://127.0.0.1:8000/docs`.

## Register a Test User

Open `POST /api/v1/auth/register`, select **Try it out**, and use synthetic data:

```json
{
  "email": "auth.demo@example.com",
  "full_name": "Auth Demo User",
  "password": "password123"
}
```

A successful response returns status `201` with the user's ID, email, name and status. It never returns the password or `hashed_password`.

The existing development-seed user has no password hash and is not intended for login. Register a separate synthetic auth user.

## Login

Open `POST /api/v1/auth/login` and submit:

```json
{
  "email": "auth.demo@example.com",
  "password": "password123"
}
```

Copy the `access_token` from the successful response. Do not copy tokens into documentation, source files or Git-tracked files.

## Authorize Swagger

1. Select **Authorize** near the top of Swagger UI.
2. Paste the access token into the HTTP Bearer value field.
3. Confirm authorization and close the dialog.
4. Open `GET /api/v1/auth/me` and select **Execute**.

The response should contain only `id`, `email`, `full_name` and `status`.

## Common Errors

- **Duplicate email — 400:** The email is already registered. Use the login endpoint or a different synthetic email.
- **Wrong password — 401:** The response is intentionally generic: `Invalid email or password.`
- **Missing token — 401:** Authorize Swagger or add an `Authorization: Bearer <token>` header.
- **Invalid or expired token — 401:** Login again to obtain a valid access token.
- **JWT configuration error:** Confirm `JWT_SECRET_KEY` is set only in the ignored `backend/.env`; never paste its value into logs or documentation.

Stop Uvicorn with `Ctrl+C` when testing is complete.
