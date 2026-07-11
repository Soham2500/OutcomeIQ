# AWS Razorpay Webhook Guide

OutcomeIQ’s Razorpay webhook must point to the deployed backend.

## Webhook URL

Use:

```text
https://api.yourdomain.com/api/v1/billing/webhook/razorpay
```

Temporary HTTP/IP URLs may be useful for non-payment testing, but real payment launch should use HTTPS.

## Test mode first

Start with:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
```

Use Razorpay test keys and test plan IDs.

## Live mode later

Only after go-live approval:

```text
PAYMENTS_LIVE_ENABLED=true
RAZORPAY_MODE=live
```

## Signature verification

Set the webhook secret only in the backend server environment:

```text
RAZORPAY_WEBHOOK_SECRET=CHANGE_ME_IN_LIGHTSAIL_ONLY
```

The backend verifies `X-Razorpay-Signature`. Invalid signatures must fail.

## Subscription source of truth

Do not trust frontend payment success. The frontend only displays a submitted/pending message.

The backend updates subscription status only after webhook verification or controlled local test activation.

## Events to enable

Enable subscription/payment lifecycle events:

- `subscription.activated`
- `subscription.charged`
- `subscription.cancelled`
- `payment.captured`
- `payment.failed`

## Rollback

If payment behavior is suspicious:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
```

Restart the backend container and verify checkout is blocked from live mode.
