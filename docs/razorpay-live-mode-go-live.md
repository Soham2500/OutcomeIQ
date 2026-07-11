# Razorpay Live Mode Go-Live Guide

Use this guide only after the MVP is stable in test mode.

## Razorpay account readiness

- Confirm KYC is completed and the account is activated.
- Add the production website link in Razorpay setup.
- Ensure the public website includes:
  - Privacy Policy
  - Terms of Use
  - Refund/Cancellation Policy
  - Contact page
- Create live Starter and Pro subscription plans in Razorpay.
- Copy live plan IDs into backend production environment variables only.

## Production webhook

Configure the Razorpay webhook URL:

```text
https://your-backend-domain/api/v1/billing/webhook/razorpay
```

Enable webhook events for subscription and payment lifecycle events, including:

- `subscription.activated`
- `subscription.charged`
- `subscription.cancelled`
- `payment.captured`
- `payment.failed`

Store the webhook secret only in the backend production environment.

## Render backend environment variables

Set placeholders first, then replace only in Render’s private environment UI:

```text
PAYMENTS_LIVE_ENABLED=true
RAZORPAY_MODE=live
RAZORPAY_CHECKOUT_ENABLED=true
RAZORPAY_KEY_ID=LIVE_KEY_ID_FROM_RAZORPAY
RAZORPAY_KEY_SECRET=LIVE_KEY_SECRET_FROM_RAZORPAY
RAZORPAY_WEBHOOK_SECRET=LIVE_WEBHOOK_SECRET
RAZORPAY_STARTER_PLAN_ID=LIVE_STARTER_PLAN_ID
RAZORPAY_PRO_PLAN_ID=LIVE_PRO_PLAN_ID
```

Do not put secret values in Git, docs, frontend variables or screenshots.

## Live transaction test

1. Deploy backend and frontend.
2. Confirm `/api/v1/health` and `/api/v1/ready`.
3. Login with a test business account.
4. Open Pricing.
5. Start Starter checkout.
6. Make a small real transaction only after approval.
7. Confirm webhook delivery in Razorpay dashboard.
8. Refresh Billing.
9. Confirm the subscription changed only after backend confirmation.

## Rollback

If anything looks wrong, immediately set:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
```

Then redeploy/restart the backend. This blocks live checkout and returns the app to test-mode behavior.

## Go-live warning

Live mode should not be enabled until legal pages, support process, refund handling, monitoring, webhook verification and rollback ownership are complete.
