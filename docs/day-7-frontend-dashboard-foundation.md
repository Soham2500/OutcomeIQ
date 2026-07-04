# OutcomeIQ — Day 7 Frontend Dashboard Foundation

## Purpose

The Day 7 frontend turns the existing OutcomeIQ APIs into a focused product surface. It supports authentication, project setup, outcome-aware dashboard analytics and human-reviewed recommendations without duplicating backend business calculations.

## Stack

- React and TypeScript
- Vite development/build tooling
- Tailwind CSS and PostCSS
- React Router
- Axios with a shared authenticated API client

The API base URL comes from `VITE_API_BASE_URL`. The committed example points to `http://127.0.0.1:8000/api/v1`; no frontend secret file is created.

## Folder Structure

```text
frontend/
├── src/
│   ├── api/             Typed API access and safe errors
│   ├── components/      Layout and reusable UI states
│   ├── pages/           Auth, dashboard, project and recommendation pages
│   ├── routes/          Token-gated protected route
│   ├── styles/          Tailwind entry stylesheet
│   └── types/           Backend response contracts
├── .env.example
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── vite.config.ts
```

## Authentication Pages

The register page submits `full_name`, `email` and `password`, then returns the user to login. Login stores only the bearer token under `outcomeiq_access_token`. The shared API client attaches it to requests without printing it. Logout removes it and redirects to login.

This local-storage approach is acceptable for the current student MVP. Production hardening such as refresh-token rotation and HTTP-only cookie strategy remains separate work.

## Dashboard Page

The dashboard loads the authenticated user’s projects, selects the first by default and allows switching projects. It consumes the four existing project analytics endpoints and presents:

- Total workflow runs and total cost
- Success rate and cost per successful outcome
- Successful and failed outcomes
- Recent run status, cost, outcome and timestamps

Loading, error, no-project and no-run states are explicit. Monetary and outcome formulas remain in the backend.

## Projects Page

The MVP form creates a simple organization and then creates a project within it. Existing projects display name, status, description and a shortened identifier. Team/member administration is deliberately excluded.

## Recommendations Page

Users select a project, generate deterministic recommendations, review severity/type/status/evidence text and dismiss open suggestions. The page does not apply recommendations or alter workflows.

## Commands

From the project root:

```powershell
.\scripts\install_frontend.ps1
.\scripts\run_frontend.ps1
.\scripts\frontend_typecheck.ps1
.\scripts\day7_frontend_foundation_verify.ps1
```

Run the backend separately before using live frontend API features. Vite serves the application at `http://127.0.0.1:5173` by default.

## Intentionally Not Implemented

- Advanced charts or exploratory analytics
- Production deployment and production auth hardening
- Real provider billing integrations
- Autonomous routing or automatic model switching
- Complete responsive/visual UX polish
- Organization membership administration

The next step is dashboard polish, small evidence-focused charts and reproducible demo data for the final presentation.
