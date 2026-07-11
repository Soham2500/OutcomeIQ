# Day 13 Razorpay Test Mode

## What was added

OutcomeIQ now has a Razorpay test-mode checkout and webhook verification foundation. Real payment mode is still not enabled.

Added:

- Safe Razorpay test configuration fields
- Backend Razorpay helper service
- Test checkout response for paid plans when Razorpay test config exists
- Local activation fallback when Razorpay is not configured
- Razorpay webhook signature verification with HMAC SHA256
- Webhook event storage in `payment_events`
- Frontend Razorpay Checkout loader/helper
- Pricing page checkout/fallback flow
- Webhook test script

## Razorpay test mode flow

1. User opens Pricing.
2. User selects Starter or Pro.
3. Backend checks whether Razorpay test checkout is configured.
4. If configured, backend creates a Razorpay test subscription and returns a safe checkout payload.
5. Frontend opens Razorpay Checkout using only `key_id`.
6. Razorpay sends webhook to backend.
7. Backend verifies signature if `RAZORPAY_WEBHOOK_SECRET` is configured.
8. Backend updates subscription status only from verified webhook data.

## Checkout flow

The frontend never receives `RAZORPAY_KEY_SECRET`. It receives only safe public checkout fields such as:

- provider
- mode
- key_id
- subscription_id
- amount
- currency
- plan_slug

## Webhook flow

Webhook URL:

```text
/api/v1/billing/webhook/razorpay
```

If a webhook secret is configured, the backend requires a valid `X-Razorpay-Signature` header. Invalid signatures return a safe `400` response.

If no webhook secret is configured, the endpoint stores the payload as an unprocessed test event.

## Local fallback activation

Local fallback activation remains available:

- Pricing page shows `Activate Test Plan Locally`
- Backend endpoint: `POST /api/v1/billing/test/activate`
- This is useful for demos without Razorpay keys

## Environment variables

```text
RAZORPAY_MODE=test
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
RAZORPAY_STARTER_PLAN_ID=
RAZORPAY_PRO_PLAN_ID=
RAZORPAY_CHECKOUT_ENABLED=false
```

Use placeholders in committed files. Put real test values only in `backend/.env` locally or Render backend environment variables.

## Why secrets stay backend-only

Razorpay key secret and webhook secret can authorize payment operations or validate payment events. They must never be sent to React, Vercel, screenshots or GitHub.

## How to test locally

1. Start backend.
2. Start frontend.
3. Open Pricing.
4. Click `Start Razorpay Test Checkout`.
5. If Razorpay is not configured, use `Activate Test Plan Locally`.
6. Test webhook storage:

```powershell
.\scripts\test_razorpay_webhook.ps1
```

If a webhook secret is configured, generate and pass a valid test signature.

## How to test after Render deployment

1. Add Razorpay test env vars to Render backend environment.
2. Set `RAZORPAY_CHECKOUT_ENABLED=true`.
3. Configure Razorpay webhook URL:

```text
https://your-backend.onrender.com/api/v1/billing/webhook/razorpay
```

4. Open Pricing on Vercel frontend.
5. Start test checkout.
6. Complete Razorpay test payment.
7. Confirm Billing page status after webhook processing.

## Intentionally not enabled

- Real Razorpay live mode
- Real money charges
- Automatic production billing
- Tax/GST invoice automation
- Real AI provider billing
