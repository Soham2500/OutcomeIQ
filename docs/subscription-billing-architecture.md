# Subscription Billing Architecture

## Overview

OutcomeIQ now has a subscription-ready billing foundation for early SaaS launch preparation. The current implementation is test/sandbox oriented only. It does not charge real money and does not call a live payment gateway.

## Plans

- Free: ₹0/month, 1 project, 50 workflow runs/month, analytics and recommendations enabled, export disabled.
- Starter: ₹499/month, 5 projects, 1000 workflow runs/month, export enabled.
- Pro: ₹1499/month, 20 projects, 10000 workflow runs/month, export enabled.

Real OpenAI provider access is intentionally disabled/future-flagged.

## Backend tables

- `plans`
- `subscriptions`
- `payment_events`
- `usage_counters`

Existing users automatically receive a Free subscription if no billing record exists.

## Billing API routes

- `GET /api/v1/billing/plans`
- `GET /api/v1/billing/me`
- `POST /api/v1/billing/checkout`
- `POST /api/v1/billing/test/activate`
- `POST /api/v1/billing/cancel`
- `POST /api/v1/billing/webhook/razorpay`
- `GET /api/v1/billing/usage`

## Test mode flow

1. User opens Pricing.
2. User selects Starter or Pro.
3. Backend returns a safe test checkout object.
4. User activates a test plan.
5. Billing page shows current plan, status and usage.

No real payment API is called.

## Future Razorpay live flow

1. Complete Razorpay KYC.
2. Add privacy policy, terms and refund/cancellation policy.
3. Store Razorpay keys only in backend environment variables.
4. Create real checkout/order/subscription from backend only.
5. Verify webhook signatures.
6. Update subscription status from verified events.

## Future Stripe flow

Stripe can follow the same provider-neutral model: backend-created checkout sessions, backend-only secrets, verified webhook events and database-backed subscriptions.

## Webhook flow

Current MVP stores Razorpay webhook payloads as unprocessed test events. Live mode must verify signatures before processing subscription changes.

## Usage limit enforcement

Backend checks:

- Project creation limit
- Monthly workflow-run limit

If a limit is reached, the backend returns:

```text
Plan limit reached. Please upgrade your subscription.
```

## Security rules

- Never store secrets in frontend code.
- Verify payment webhooks before live processing.
- Backend controls access and limits.
- Do not trust frontend plan state.
- Do not commit `.env` files.
