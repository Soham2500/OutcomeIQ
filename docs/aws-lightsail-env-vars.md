# AWS Lightsail Environment Variables

Use `backend/.env.aws.example` as the server-only template. On Lightsail, copy it to:

```text
backend/.env
```

Never commit `backend/.env`.

## Core backend variables

```text
APP_NAME=OutcomeIQ API
APP_VERSION=0.1.0
ENVIRONMENT=production
API_V1_PREFIX=/api/v1
BACKEND_CORS_ORIGINS=https://your-amplify-domain.amplifyapp.com,https://yourdomain.com
DATABASE_URL=postgresql+psycopg2://outcomeiq_user:CHANGE_ME@postgres:5432/outcomeiq_prod
JWT_SECRET_KEY=CHANGE_ME_STRONG_SECRET
```

## PostgreSQL container variables

```text
POSTGRES_DB=outcomeiq_prod
POSTGRES_USER=outcomeiq_user
POSTGRES_PASSWORD=CHANGE_ME
```

The `DATABASE_URL` password and `POSTGRES_PASSWORD` must match.

## Razorpay variables

```text
PAYMENTS_LIVE_ENABLED=false
BILLING_PROVIDER_MODE=test
RAZORPAY_MODE=test
RAZORPAY_CHECKOUT_ENABLED=true
RAZORPAY_KEY_ID=rzp_test_placeholder
RAZORPAY_KEY_SECRET=CHANGE_ME_IN_LIGHTSAIL_ONLY
RAZORPAY_WEBHOOK_SECRET=CHANGE_ME_IN_LIGHTSAIL_ONLY
RAZORPAY_STARTER_PLAN_ID=plan_placeholder
RAZORPAY_PRO_PLAN_ID=plan_placeholder
```

Use test keys first. Live mode requires:

```text
PAYMENTS_LIVE_ENABLED=true
RAZORPAY_MODE=live
```

Do not enable this until go-live checks are complete.

## Public app/admin variables

```text
APP_PUBLIC_URL=https://yourdomain.com
SUPPORT_EMAIL=support@yourdomain.com
ADMIN_EMAILS=admin@yourdomain.com
```

## Simulated AI mode

```text
AI_PROVIDER_MODE=simulated
OPENAI_API_KEY=
OPENAI_DEFAULT_MODEL=
```

The early live MVP should remain simulated until budget limits, provider logging and kill switches are implemented.

## Secret safety rules

- Never place secrets in frontend environment variables.
- Never commit `backend/.env`.
- Never commit Razorpay key CSV files.
- Never commit AWS credentials.
- Rotate any secret that was accidentally copied into chat, screenshots or Git.
