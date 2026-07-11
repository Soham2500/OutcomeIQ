# Early Live Launch Plan

## Phase 1: Safe live website

- Deploy backend on Render.
- Deploy PostgreSQL on Render.
- Deploy frontend on Vercel.
- Configure environment variables.
- Configure CORS for the frontend domain.
- Verify `/api/v1/health`.
- Run production smoke checks.

## Phase 2: Test subscription mode

- Pricing page live.
- Billing page live.
- Test subscription activation only.
- No real payment enabled.
- No real AI-provider billing enabled.

## Phase 3: Real payment readiness

- Razorpay KYC.
- Privacy policy.
- Terms and conditions.
- Refund/cancellation policy.
- Verified live webhook.
- Real payments enabled only after production verification.

## Launch checklist

- Backend health works.
- Frontend loads.
- Register/login works.
- Create project works.
- Run demo data works.
- Dashboard works.
- Pricing page works.
- Billing page works.
- No secrets exposed.
- Webhook endpoint is protected before live processing.

## MVP boundary

The first live launch should remain simulated-provider only. Real AI provider usage and live payments are future steps.
