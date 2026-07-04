# OutcomeIQ — Day 4 Manual API Testing

## 1. Run the Backend

```powershell
cd C:\Users\soham\OneDrive\Documents\pro
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
uvicorn app.main:app --reload
```

## 2. Open Swagger

Open `http://127.0.0.1:8000/docs`.

## 3. Register a Synthetic User

Use `POST /api/v1/auth/register`. Never use production credentials:

```json
{
  "email": "manual.api@example.com",
  "full_name": "Manual API User",
  "password": "TestPassword123!"
}
```

The JSON keys must be exactly `email`, `full_name` and `password` (`fullName` is not accepted). Normal addresses use standard email validation; local development also permits the controlled `@outcomeiq.local` domain.

## 4. Login

Call `POST /api/v1/auth/login` and copy the returned `access_token`:

```json
{
  "email": "manual.api@example.com",
  "password": "TestPassword123!"
}
```

## 5. Authorize

Select **Authorize** in Swagger, paste the token into the HTTP Bearer field and confirm.

## 6. Verify Current User

Call `GET /api/v1/auth/me`. Confirm the returned email matches the registered user and that no password field is present.

## 7. Create an Organization

Call `POST /api/v1/organizations`:

```json
{
  "name": "Swagger Demo Organization",
  "slug": "swagger-demo-org"
}
```

Copy the returned organization `id`.

## 8. Create a Project

Call `POST /api/v1/projects`, replacing the example organization ID:

```json
{
  "organization_id": "REPLACE_WITH_ORGANIZATION_ID",
  "name": "Swagger Demo Project",
  "slug": "swagger-demo-project",
  "description": "Synthetic manual API test"
}
```

Copy the returned project `id`.

## 9. Get the Project

Call `GET /api/v1/projects/{project_id}` with the returned project ID. Membership is now required; the creator succeeds because project creation added the owner membership.

## 10. Patch the Project

Call `PATCH /api/v1/projects/{project_id}` as the owner:

```json
{
  "name": "Swagger Demo Project Updated",
  "description": "Updated through the owner-authorized endpoint",
  "status": "active"
}
```

Only project owners and admins may update a project.

## 11. List Projects

Call `GET /api/v1/projects`. The response is scoped to projects where the current user has a membership. Optionally set `organization_id` and use `limit`/`offset`.

## 12. Check Project Members

Call `GET /api/v1/projects/{project_id}/members`. The registered user should appear with role `owner`.

## 13. Common Errors

- **401:** Missing, invalid or expired bearer token. Login again and reauthorize Swagger.
- **400 organization slug:** The organization slug already exists or violates lowercase slug validation.
- **400 project slug:** That slug already exists in the selected organization.
- **404 organization:** The supplied organization UUID does not exist.
- **404 project:** The supplied project UUID does not exist.
- **403 active user required:** The authenticated account is inactive or suspended.
- **403 project membership required:** The authenticated user is not a member of that project.
- **403 owner/admin required:** A member or viewer attempted to patch the project.
- **422:** Request validation failed, commonly because a UUID or lowercase slug is malformed.
- **422 during registration:** Confirm the request is JSON with `email`, `full_name` and `password`, and that `Content-Type` is `application/json`.

Project reads, updates and member lists now enforce existing project memberships and roles. Organization endpoints still use active-user-only authorization and require a future organization membership model/policy. Use only local synthetic data.
