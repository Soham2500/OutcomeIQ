# Razorpay Test Mode Setup

## Purpose

This guide prepares OutcomeIQ for future Razorpay testing without enabling real payments.

## Steps

1. Create a Razorpay account.
2. Switch to test mode.
3. Generate test mode keys from the Razorpay dashboard.
4. Create test subscription plans in Razorpay for Starter and Pro.
5. Copy the test plan IDs.
6. Store keys and plan IDs only in `backend/.env` locally or Render backend environment variables.
7. Never place Razorpay secrets in frontend files.
8. Configure webhook URL:

```text
/api/v1/billing/webhook/razorpay
```

9. Add webhook secret to backend environment.
10. Test checkout creation from the backend.
11. Send a test webhook.
12. Verify webhook signature verification.
13. Verify `payment_events` stores the payload.
14. Verify subscription status is updated only after verified webhook data.

## Test environment variables

```text
RAZORPAY_MODE=test
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxx
RAZORPAY_KEY_SECRET=your_test_secret
RAZORPAY_WEBHOOK_SECRET=your_test_webhook_secret
RAZORPAY_STARTER_PLAN_ID=plan_test_starter
RAZORPAY_PRO_PLAN_ID=plan_test_pro
RAZORPAY_CHECKOUT_ENABLED=true
```

Use placeholders in documentation and committed examples. Never commit real values.

## Current MVP behavior

OutcomeIQ supports local test-plan activation when Razorpay is not configured. When Razorpay test variables and plan IDs are configured, the backend can create a test subscription checkout payload. Live mode remains disabled.

## Switching from fallback to Razorpay test checkout

1. Add Razorpay test keys and test plan IDs to backend environment.
2. Set `RAZORPAY_CHECKOUT_ENABLED=true`.
3. Restart/redeploy backend.
4. Open Pricing.
5. Select Starter or Pro.
6. Razorpay Checkout should open in test mode.
7. Confirm subscription status only after webhook confirmation.

## Before switching live

- Complete Razorpay KYC.
- Publish privacy policy.
- Publish terms and conditions.
- Publish refund/cancellation policy.
- Implement and test webhook signature verification.
- Run production smoke checks.
- Confirm no secrets are exposed in frontend bundles or Git history.
