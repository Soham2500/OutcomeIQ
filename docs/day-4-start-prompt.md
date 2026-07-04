# Day 4 — Authentication Foundation

You are my senior backend engineer and authentication security mentor.

Project: OutcomeIQ — Outcome-aware AI FinOps Platform

Project root: `C:\Users\soham\OneDrive\Documents\pro`

Current foundation:

- FastAPI modular monolith
- PostgreSQL connected
- Alembic at `0002_core_identity_projects (head)`
- Core `users` table and repository exist
- `hashed_password` is nullable during the transition
- Pydantic user schemas currently expose no password fields
- Demo user contains no password hash

Your task is to implement the Day 4 authentication foundation.

Required work:

1. Review the existing architecture, user model, schemas, repository, settings and API router.
2. Select and add appropriate password-hashing and JWT dependencies explicitly.
3. Implement a password hashing and verification utility.
4. Create authentication schemas for registration, login and access-token responses.
5. Create an authentication service that handles duplicate registration and invalid credentials safely.
6. Create a register endpoint.
7. Create a login endpoint.
8. Create JWT access-token generation and validation utilities using environment-backed settings.
9. Create a current-user dependency placeholder suitable for protected routes.
10. Add focused unit and API tests, including rejection paths.
11. Update documentation and verification scripts.

Security requirements:

- Never expose `hashed_password` in any response, schema, log or exception.
- Never log or persist raw passwords.
- Never hardcode or print the JWT secret.
- Never modify or commit `backend/.env`.
- Use only synthetic test credentials.
- Return generic invalid-credential responses.
- Keep token expiry configurable.

Boundaries:

- Do not create frontend code.
- Do not implement organization or project authorization APIs.
- Do not create workflow, cost, outcome or recommendation APIs/tables.
- Do not add OAuth, password reset, email verification, refresh tokens or enterprise SSO yet.
- Do not run destructive database commands.

After implementation, confirm the files changed, dependencies added, endpoints created, test results, security assumptions and the next recommended Day 4 step.
