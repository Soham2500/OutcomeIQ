# OutcomeIQ — Launch Notes Template

> Copy this template for a specific release. Use public URLs and sanitized facts only; never add credentials, tokens or private database URLs.

## Release Identity

- **Project name:** OutcomeIQ — Outcome-aware AI FinOps Platform
- **Launch version:** v0.1 MVP
- **Launch date:** YYYY-MM-DD
- **Deployment owner:** `<OWNER>`
- **Deployed commit:** `<COMMIT_SHA>`
- **Live period:** `<START_DATE>` to `<END_DATE>`

## Live URLs

- **Frontend:** `https://YOUR_FRONTEND_DOMAIN`
- **Backend health:** `https://YOUR_BACKEND_DOMAIN/api/v1/health`
- **API docs:** `https://YOUR_BACKEND_DOMAIN/docs`

## MVP Features

- Authentication
- Organizations and projects
- Workflow and configuration registry
- Workflow/model/tool call logging
- Deterministic cost calculation
- Outcome Contract and outcome tracking
- Dashboard analytics and cost per successful outcome
- Rule-based, evidence-backed recommendations
- Docker local production-like setup
- Simulated AI provider

## Demo Story

OutcomeIQ shows why the cheapest AI request is not always the cheapest successful business outcome. The customer-support scenario connects complete workflow cost, retries and failures to verified ticket outcomes, then compares configurations using cost per successful outcome.

## Verification Summary

- **Pre-deploy check:** `<PASSED / NOT RUN>`
- **Production smoke check:** `<PASSED / NOT RUN>`
- **Manual registration/login:** `<PASSED / NOT RUN>`
- **Dashboard and recommendations:** `<PASSED / NOT RUN>`
- **Go-live checklist:** `<COMPLETE / INCOMPLETE>`

## Known Limitations

- No real AI-provider calls yet
- No real provider billing synchronization yet
- No advanced ML-based recommendations yet
- No production-grade centralized monitoring yet
- No automated CI/CD yet
- Recommendations remain rule-based and human-reviewed
- Public MVP uses only synthetic demonstration data

## Operational Notes

- **Hosting:** `<BACKEND_HOST / FRONTEND_HOST / DATABASE_HOST>`
- **Rollback release:** `<PREVIOUS_WORKING_COMMIT_OR_DEPLOYMENT>`
- **Planned shutdown/review date:** `<YYYY-MM-DD>`
- **Known non-sensitive issues:** `<ISSUE_SUMMARY>`

## Next Steps

- Add monitoring and alerting before longer-term operation.
- Review usage and cost during the one-month live period.
- Add real AI APIs only after token limits, monthly budget caps, model allowlists, complete call logging and a provider kill switch are implemented.
- Preserve OutcomeIQ's evidence-backed, human-reviewed decision boundary.
