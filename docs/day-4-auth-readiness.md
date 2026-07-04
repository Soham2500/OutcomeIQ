# OutcomeIQ — Day 4 Authentication Readiness

## Readiness Status

This checklist was satisfied at Day 3 closure. The basic authentication foundation is now implemented; current details are recorded in `day-4-checkpoint.md`.

The backend is ready to begin a narrowly scoped authentication foundation:

- PostgreSQL is connected and Alembic is at `0002_core_identity_projects (head)`.
- The `users` table exists.
- `users.hashed_password` exists and is nullable for the current transition stage.
- The demo user contains no real password and currently has no password hash.
- `UserCreate` and `UserRead` expose neither raw nor hashed passwords.
- Core repository and session foundations are available.
- At Day 3 closure, authentication, login and registration APIs had not yet been created.
- `JWT_SECRET_KEY` exists as an optional configuration placeholder in `.env.example`.

## Day 4 Tasks

1. Add a password hashing and verification utility using an approved password-hashing library.
2. Create authentication-specific request and response schemas.
3. Create an authentication service with explicit duplicate-user and invalid-credential behavior.
4. Add a registration endpoint.
5. Add a login endpoint.
6. Add JWT access-token generation and validation utilities.
7. Add a current-user dependency placeholder for protected routes.
8. Add focused unit and API tests for successful and rejected authentication paths.

## Safety Rules

- Never expose `hashed_password` in schemas, responses, logs or exceptions.
- Never store or log raw passwords.
- Never commit `.env` or any local secret.
- Never hardcode the JWT secret in source code, tests or documentation.
- Use only synthetic test users and isolated test credentials.
- Keep access-token lifetimes configurable.
- Do not mix project authorization or workflow APIs into the authentication milestone.

## Start Condition

Before implementation, select the password-hashing and JWT libraries deliberately, update dependencies explicitly, and define test-only secret handling. Day 4 should remain an authentication foundation—not a full authorization system.
