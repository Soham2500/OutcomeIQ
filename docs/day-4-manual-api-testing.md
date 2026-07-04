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

Use `POST /api/v1/auth/register` with a synthetic email and password. Never use production credentials.

## 4. Login

Call `POST /api/v1/auth/login` with the same credentials and copy the returned `access_token`.

## 5. Authorize

Select **Authorize** in Swagger, paste the token into the HTTP Bearer field and confirm.

## 6. Create an Organization

Call `POST /api/v1/organizations`:

```json
{
  "name": "Swagger Demo Organization",
  "slug": "swagger-demo-org"
}
```

Copy the returned organization `id`.

## 7. Create a Project

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

## 8. List Projects

Call `GET /api/v1/projects`. Optionally set `organization_id` to the organization created above. Use `limit` and `offset` to test pagination.

## 9. Check Project Members

Call `GET /api/v1/projects/{project_id}/members`. The registered user should appear with role `owner`.

## 10. Common Errors

- **401:** Missing, invalid or expired bearer token. Login again and reauthorize Swagger.
- **400 organization slug:** The organization slug already exists or violates lowercase slug validation.
- **400 project slug:** That slug already exists in the selected organization.
- **404 organization:** The supplied organization UUID does not exist.
- **404 project:** The supplied project UUID does not exist.
- **422:** Request validation failed, commonly because a UUID or lowercase slug is malformed.

Current authorization permits any active authenticated user to access these APIs. Use only local synthetic data until tenant and role checks are implemented.
