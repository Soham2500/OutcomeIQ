# Production Payment Go-Live Checklist

OutcomeIQ must not enable live payments until every item below is reviewed and approved.

## Required before enabling live payments

- Razorpay/processor account KYC completed.
- Business name, address, support email and tax details verified.
- Privacy policy reviewed and published.
- Terms of use reviewed and published.
- Refund/cancellation policy reviewed and published.
- Contact/support route published and monitored.
- Production webhook endpoint configured.
- Webhook signature verification tested with real provider test tools.
- `PAYMENTS_LIVE_ENABLED` intentionally set only after approval.
- Payment provider mode intentionally changed from `test` only after approval.
- Backend secrets stored only in production environment variables.
- No payment secrets stored in frontend variables or source code.
- Admin billing access restricted through `ADMIN_EMAILS`.
- Production smoke test completed.
- Rollback plan confirmed.

## Current MVP policy

Real payments are disabled. Test checkout and local test activation are the only supported billing flows.

If live mode is attempted while `PAYMENTS_LIVE_ENABLED=false`, the backend must return:

```text
Live payments are disabled. Use test mode until launch approval is complete.
```

## Final approval record

Before enabling live payments, record:

- Approver name:
- Date:
- Payment provider:
- Production webhook URL:
- Rollback owner:
- Support email:
- Notes:
