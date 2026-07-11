# Day 15 Payment Gateway On

## Objective

Day 15 completes the backend-controlled Razorpay checkout flow while preserving OutcomeIQ launch safety. The frontend can open Razorpay Checkout, but subscription entitlement remains controlled by the backend through verified webhooks or explicit local test activation.

## What was added

- Safer Razorpay configuration checks.
- Live-payment guard:
  - `PAYMENTS_LIVE_ENABLED=false` blocks live checkout.
  - `RAZORPAY_MODE=live` works only when the live flag is explicitly enabled.
- Generic Razorpay subscription checkout helper:
  - supports `starter`
  - supports `pro`
  - maps plans to backend env plan IDs
- Safe checkout payload returned to frontend:
  - public `key_id`
  - `subscription_id`
  - plan and amount metadata
  - prefill name/email
  - no secret key
- Backend webhook verification using HMAC SHA256.
- Duplicate webhook-event protection by provider event ID.
- Pricing/Billing UX messages explaining webhook confirmation.
- Local test activation remains available for demos.

## How Razorpay checkout works

1. User opens Pricing.
2. User selects Starter or Pro.
3. Frontend calls `POST /api/v1/billing/checkout`.
4. Backend checks plan, mode, environment variables and live-payment guard.
5. Backend creates a Razorpay subscription when configured.
6. Frontend opens Razorpay Checkout using only safe public fields.
7. Browser success shows a submitted/waiting message.
8. Backend webhook verifies the event and updates subscription state.

Frontend payment success is not final. The backend is the source of truth.

## Required backend environment variables

Use backend environment variables only:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
RAZORPAY_CHECKOUT_ENABLED=true
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
RAZORPAY_STARTER_PLAN_ID=
RAZORPAY_PRO_PLAN_ID=
```

Never commit private keys, CSV exports or webhook secrets. Do not place Razorpay secret keys in the frontend.

## Test mode

For test mode:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
RAZORPAY_CHECKOUT_ENABLED=true
```

Use Razorpay test key ID, test key secret and test subscription plan IDs in the backend environment.

If Razorpay is not configured, the app returns a safe fallback message and the user can use local test activation.

## Live mode

Live checkout requires both:

```text
PAYMENTS_LIVE_ENABLED=true
RAZORPAY_MODE=live
```

If live mode is requested while the live flag is false, checkout is rejected with:

```text
Live payments are disabled. Use test mode until launch approval is complete.
```

## Webhook activation

Webhook endpoint:

```text
POST /api/v1/billing/webhook/razorpay
```

If `RAZORPAY_WEBHOOK_SECRET` is configured, the backend verifies the `X-Razorpay-Signature` header before processing.

Handled events include:

- `subscription.activated`
- `subscription.charged`
- `subscription.cancelled`
- `payment.captured`
- `payment.failed`

## Manual test flow

1. Configure backend Razorpay test environment variables.
2. Start backend.
3. Start frontend.
4. Login.
5. Open Pricing.
6. Click Starter or Pro.
7. Complete Razorpay Checkout in test mode.
8. Wait for webhook confirmation.
9. Open Billing and refresh.
10. Confirm subscription status, provider and usage.

If webhook is not configured, use local test activation for demo continuity.

## Verification

Run from project root:

```powershell
.\scripts\day15_payment_gateway_verify.ps1
```

Expected final line:

```text
DAY 15 PAYMENT GATEWAY VERIFY PASSED
```

## Intentionally not enabled by default

- Live payment capture.
- Automatic commercial go-live.
- Frontend secret storage.
- Real AI provider billing.
- Production legal approval.
- Refund automation.
- Full enterprise billing reconciliation.
