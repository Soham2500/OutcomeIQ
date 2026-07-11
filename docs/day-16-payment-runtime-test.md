# Day 16 Payment Runtime Test

## Objective

Day 16 verifies OutcomeIQ billing behavior at runtime without charging real money. Day 15 proves code/build readiness; Day 16 proves the running app responds safely for billing, checkout fallback, webhook behavior and payment UX.

## Automated runtime smoke

Start the backend first, then run:

```powershell
.\scripts\day16_payment_runtime_smoke.ps1
```

Optional backend URL:

```powershell
.\scripts\day16_payment_runtime_smoke.ps1 -BackendUrl "http://127.0.0.1:8000"
```

The smoke script checks:

- `GET /api/v1/health`
- protected billing endpoint behavior
- webhook endpoint behavior with a fake unsigned payload

It does not use real Razorpay payment IDs, does not charge money and does not print secrets.

## Manual browser test flow

1. Start the app with Docker or local backend/frontend scripts.
2. Open the frontend.
3. Login or register.
4. Open the Pricing page.
5. Check that Free, Starter and Pro plans are visible.
6. Click Starter checkout.
7. If Razorpay is configured:
   - Razorpay Checkout should open.
   - It should use test mode when backend env is test.
   - After payment success, UI should show: `Payment submitted. Subscription will activate after secure webhook confirmation.`
8. If Razorpay is not configured:
   - UI should show the safe fallback message.
   - `Activate Test Plan Locally` should remain available.
9. Open Billing.
10. Confirm current plan, subscription status, provider, billing mode and usage appear.
11. Run demo data.
12. Confirm usage count changes if usage tracking is enabled for that flow.
13. Confirm Dashboard still works.

## Expected UX

- Test backend mode should display `Test Mode`.
- Live backend mode should display `Live Payment`.
- Billing should not show raw JSON.
- Pricing and Billing should not expose secrets.
- Frontend payment success should not directly activate subscription.
- Subscription activation should happen through backend webhook verification or controlled local test activation.

## Webhook behavior

Webhook endpoint:

```text
POST /api/v1/billing/webhook/razorpay
```

If `RAZORPAY_WEBHOOK_SECRET` is configured, an invalid or missing signature should fail safely with HTTP 400.

If `RAZORPAY_WEBHOOK_SECRET` is not configured in local development, the endpoint may store the fake event safely without changing any paid subscription unless a matching subscription exists and a verified signature is provided.

## Live-payment warning

Do not use live cards during test mode.

Do not enable:

```text
PAYMENTS_LIVE_ENABLED=true
```

until deployment, webhook verification, policy pages, KYC/go-live checklist and rollback ownership are complete.

## Verification

Run:

```powershell
.\scripts\day16_payment_runtime_verify.ps1
```

Expected final line:

```text
DAY 16 PAYMENT RUNTIME VERIFY PASSED
```
