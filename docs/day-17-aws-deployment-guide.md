# Day 17 AWS Deployment Guide

OutcomeIQ’s recommended early live architecture is intentionally simple:

- Frontend: AWS Amplify Hosting
- Backend: Dockerized FastAPI on AWS Lightsail
- Database: PostgreSQL container on the same Lightsail instance
- Payments: Razorpay test/live-ready webhook

This avoids expensive early infrastructure such as ECS/Fargate, ALB, NAT Gateway and RDS.

## Part A: AWS cost safety

1. Enable MFA on the AWS root account.
2. Create an AWS Budget alert before launching resources.
3. Start with the smallest suitable Lightsail instance.
4. Use one Lightsail instance for backend and PostgreSQL during MVP validation.
5. Avoid ECS/Fargate, RDS, ALB and NAT Gateway unless the MVP proves demand.
6. Stop or delete unused instances, snapshots and static IPs.
7. Check the AWS Billing dashboard weekly.

## Part B: Create Lightsail instance

1. Open AWS Lightsail.
2. Create an Ubuntu instance.
3. Choose the smallest suitable plan first.
4. Attach a static IP.
5. Open firewall ports:
   - `22` for SSH
   - `80` for HTTP
   - `443` for HTTPS when domain/reverse proxy is configured
   - `8000` temporarily for backend testing only

For real payment launch, HTTPS is strongly recommended.

## Part C: Deploy backend/database

1. SSH into Lightsail.
2. Run `scripts/aws_lightsail_server_setup.sh`.
3. Log out and SSH back in.
4. Clone the GitHub repo into `/opt/outcomeiq`.
5. Copy `backend/.env.aws.example` to `backend/.env` on the server.
6. Replace placeholders manually in `backend/.env`.
7. Start services:

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

8. Run migrations:

```bash
docker compose -f docker-compose.aws.yml exec backend alembic upgrade head
```

9. Seed plans/pricing using the existing reviewed project process.
10. Test health:

```bash
curl http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1/health
curl http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1/ready
```

## Part D: Deploy frontend on AWS Amplify

1. Open AWS Amplify Hosting.
2. Connect the GitHub repository.
3. Set app root to `frontend`.
4. Use build command:

```bash
npm run build
```

5. Set output directory:

```text
dist
```

6. Add environment variable:

```text
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

For temporary testing, use:

```text
VITE_API_BASE_URL=http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1
```

7. Add Amplify SPA rewrite to `/index.html` if required by the AWS console.

## Part E: CORS setup

Add the Amplify URL to backend CORS:

```text
BACKEND_CORS_ORIGINS=https://your-amplify-domain.amplifyapp.com,https://yourdomain.com
```

Restart backend after changing environment variables:

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

## Part F: Razorpay webhook

Webhook URL:

```text
https://api.yourdomain.com/api/v1/billing/webhook/razorpay
```

Use test mode first:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
```

Enable live mode only after webhook verification, policy pages, HTTPS and rollback checks are complete.

## Part G: Smoke test

From your local machine:

```powershell
.\scripts\aws_live_smoke_check.ps1 -BackendUrl "https://api.yourdomain.com" -FrontendUrl "https://your-amplify-domain.amplifyapp.com"
```

Temporary non-HTTPS backend testing:

```powershell
.\scripts\aws_live_smoke_check.ps1 -BackendUrl "http://YOUR_LIGHTSAIL_STATIC_IP:8000" -FrontendUrl "https://your-amplify-domain.amplifyapp.com"
```

## Part H: Manual browser test

1. Open the Amplify frontend.
2. Register or login.
3. Create a project.
4. Run demo data.
5. Open Dashboard.
6. Open Pricing.
7. Start Razorpay test checkout.
8. Open Billing and verify plan/status/provider/mode.
9. Confirm recommendations/dashboard still work.

## Part I: Rollback

If anything looks wrong:

1. Set:

```text
PAYMENTS_LIVE_ENABLED=false
RAZORPAY_MODE=test
```

2. Restart backend:

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

3. Revert the latest Git commit if the issue is application-code related.
4. Disable Razorpay live webhook if needed.
5. Keep PostgreSQL volume intact unless deliberately restoring from backup.
