# OutcomeIQ — Day 4 Organization and Project APIs

## Purpose

This API slice exposes the existing organization, project and project-membership persistence layer to authenticated users. It creates no new table or migration.

Authentication is enforced on every endpoint in this document. Authorization is intentionally coarse for this milestone: any active authenticated user can list, read, create and update organizations and projects. Tenant membership and role-based permission checks must be added before production use.

## Organization Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/organizations` | Create an organization and audit event |
| GET | `/api/v1/organizations` | List organizations with `limit` and `offset` |
| GET | `/api/v1/organizations/{organization_id}` | Read one organization |
| PATCH | `/api/v1/organizations/{organization_id}` | Update organization name/status and audit the change |

Create request:

```json
{
  "name": "Acme Payments",
  "slug": "acme-payments"
}
```

Update request:

```json
{
  "name": "Acme Payments India",
  "status": "active"
}
```

Slugs accept lowercase letters, digits and single hyphen-separated segments. Duplicate organization slugs return `400`; unknown organization IDs return `404`.

## Project Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/projects` | Create a project, owner membership and audit event |
| GET | `/api/v1/projects` | List projects, optionally filtered by `organization_id` |
| GET | `/api/v1/projects/{project_id}` | Read one project |
| PATCH | `/api/v1/projects/{project_id}` | Update project fields and audit the change |
| GET | `/api/v1/projects/{project_id}/members` | List project memberships |

Create request:

```json
{
  "organization_id": "00000000-0000-0000-0000-000000000000",
  "name": "AI Customer Support",
  "slug": "ai-customer-support",
  "description": "OutcomeIQ support workflow project"
}
```

Replace the example UUID with the ID returned by the organization create endpoint.

Update request:

```json
{
  "name": "AI Support Operations",
  "description": "Updated synthetic demo project",
  "status": "active"
}
```

Creating a project automatically adds the current user as `owner`. Project slugs are unique within an organization. An unknown organization/project returns `404`; a duplicate project slug within the organization returns `400`.

## Audit Behavior

Organization/project creation and non-empty updates append safe audit events containing the actor, relevant organization/project identifiers, entity type and a generic message. Update metadata contains field names only—never secrets or raw request payloads.

## Swagger Testing

1. Register and log in through the auth endpoints.
2. Copy the access token and use Swagger's **Authorize** button.
3. Create an organization and copy its ID.
4. Create a project with that organization ID.
5. List projects and inspect the project's members.

See `docs/day-4-manual-api-testing.md` for the complete sequence.

## Authorization Boundary

Current access is authentication-only. Organization ownership, organization membership, project membership enforcement, owner/admin/member/viewer permissions and cross-tenant isolation are not yet implemented at the API layer. This limitation is explicit and must be resolved before production deployment.

## Intentionally Not Implemented

- Organization invitations or organization-member APIs
- Advanced project RBAC or permission checks
- Project-member add/update/remove endpoints
- Delete endpoints
- Workflow, cost, outcome, comparison or recommendation APIs
- Frontend code
