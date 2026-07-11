# Admin Billing View Guide

The admin billing view gives a safe read-only operational snapshot for launch review.

## Backend endpoints

- `GET /api/v1/admin/billing/overview`
- `GET /api/v1/admin/billing/subscriptions`
- `GET /api/v1/admin/billing/payment-events`
- `GET /api/v1/admin/billing/usage`

## Frontend route

- `/admin/billing`

The route is intentionally hidden from the sidebar. It can be opened manually by an authorized admin.

## Access control

Admin access is controlled by the backend `ADMIN_EMAILS` environment variable. It accepts a comma-separated email allowlist.

Example placeholder:

```text
ADMIN_EMAILS=admin@example.com
```

Do not commit real admin emails if that list is private.

## Safety behavior

- Non-admin users receive a safe `403` response.
- Raw payment payloads are not returned.
- Provider IDs are masked.
- Secrets are never shown.
- No billing state is changed by these endpoints.

## Future work

A production version should replace config-based admin access with proper role-based authorization, audit logs and organization-scoped billing controls.
