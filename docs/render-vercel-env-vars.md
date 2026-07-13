# Render and Vercel Environment Variables

This guide lists the environment variables required for early live deployment. Do not commit real secrets to GitHub.

## Render Backend Environment Variables

Set these in the Render dashboard for the backend Web Service:

```text
APP_ENV=production
DEBUG=false
SECRET_KEY=generate_strong_secret_key
DATABASE_URL=Render PostgreSQL internal database URL
BACKEND_CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173,http://127.0.0.1:8080
ACCESS_TOKEN_EXPIRE_MINUTES=1440
LOG_LEVEL=INFO
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
DEFAULT_AI_PROVIDER=gemini
DEFAULT_AI_MODEL=gemini-2.5-flash
DEFAULT_OPENAI_MODEL=gpt-4o-mini
DEFAULT_GEMINI_MODEL=gemini-2.5-flash
COST_CURRENCY=INR
USD_TO_INR_RATE=83.50
AI_PROVIDER_TIMEOUT_SECONDS=60
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_gmail_address
SMTP_PASSWORD=your_gmail_app_password
MAIL_FROM=your_gmail_address
MAIL_FROM_NAME=OutcomeIQ
OTP_EXPIRE_MINUTES=10
OTP_RESEND_COOLDOWN_SECONDS=60
```

For Gmail SMTP, use a Gmail app password from the deployment owner's Google account. Do not use or commit the normal Gmail account password.

If using the subscription-ready billing foundation in test mode:

```text
BILLING_PROVIDER_MODE=test
RAZORPAY_MODE=test
RAZORPAY_KEY_ID=optional_test_key
RAZORPAY_KEY_SECRET=optional_test_secret
RAZORPAY_WEBHOOK_SECRET=optional_test_webhook_secret
RAZORPAY_STARTER_PLAN_ID=optional_test_starter_plan_id
RAZORPAY_PRO_PLAN_ID=optional_test_pro_plan_id
RAZORPAY_CHECKOUT_ENABLED=false
```

The Razorpay variables above are optional for the current MVP. Keep `RAZORPAY_CHECKOUT_ENABLED=false` until you intentionally test Razorpay sandbox checkout. Live payment mode is not enabled.

## Vercel Frontend Environment Variables

Set this in the Vercel project settings:

```text
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com/api/v1
```

## Important notes

- Never add backend secrets to Vercel frontend environment variables.
- Only the public API base URL goes to the frontend.
- `DATABASE_URL`, `SECRET_KEY`, provider API keys, and SMTP credentials belong only in the Render backend environment.
- Use the Render and Vercel dashboards for secrets, not GitHub files.
- Do not paste secrets into screenshots, documentation, README files or commits.
