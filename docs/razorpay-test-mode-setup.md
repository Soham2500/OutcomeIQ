# Razorpay Test Mode Setup

## Purpose

This guide prepares OutcomeIQ for future Razorpay testing without enabling real payments.

## Steps

1. Create a Razorpay account.
2. Switch to test mode.
3. Generate test mode keys.
4. Store keys only in `backend/.env` locally or Render backend environment variables.
5. Never place Razorpay keys in frontend files.
6. Configure webhook URL:

```text
/api/v1/billing/webhook/razorpay
```

7. Test checkout creation from the backend.
8. Send a test webhook.
9. Verify `payment_events` stores the payload.
10. Verify subscription status only after webhook signature checks are implemented.

## Current MVP behavior

OutcomeIQ currently returns a provider-neutral test checkout response and supports local test-plan activation. It does not call Razorpay live APIs.

## Before switching live

- Complete Razorpay KYC.
- Publish privacy policy.
- Publish terms and conditions.
- Publish refund/cancellation policy.
- Implement and test webhook signature verification.
- Run production smoke checks.
- Confirm no secrets are exposed in frontend bundles or Git history.
