# AWS Deployment Quickstart

OutcomeIQ early deployment target:

- Frontend: AWS Amplify
- Backend: AWS Lightsail Ubuntu server
- Database: PostgreSQL Docker container on Lightsail
- Runtime: Docker Compose
- Payments: Razorpay through backend environment variables only

## A. Create AWS Budget alert

Before creating resources, create an AWS Budget alert so Lightsail/Amplify usage stays inside credits.

## B. Create Lightsail Ubuntu instance

Create a low-cost Ubuntu Lightsail instance first. Attach a static IP.

Open ports:

- `22` for SSH
- `8000` temporarily for backend testing
- `80` and `443` later when adding a domain/reverse proxy

## C. SSH into server

```bash
ssh ubuntu@YOUR_LIGHTSAIL_STATIC_IP
```

## D. Install Docker using script

Copy or upload `scripts/aws_lightsail_server_setup.sh`, then run:

```bash
bash aws_lightsail_server_setup.sh
```

Log out and SSH back in after the script finishes.

## E. Clone GitHub repo

```bash
cd /opt/outcomeiq
git clone https://github.com/Soham2500/OutcomeIQ.git .
```

## F. Manually create backend/.env on server

```bash
cp backend/.env.aws.example backend/.env
nano backend/.env
```

Replace placeholders on the server only. Never commit `backend/.env`.

## G. Start backend and PostgreSQL

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

## H. Run migrations

```bash
docker compose -f docker-compose.aws.yml exec backend alembic upgrade head
```

## I. Seed plans/pricing if scripts exist

Use the existing reviewed seed process for plans/pricing before testing Pricing.

## J. Deploy frontend on AWS Amplify

In Amplify:

- App root: `frontend`
- Build file: `frontend/amplify.yml`
- Build command: `npm run build`
- Output directory: `dist`

Add:

```text
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

Temporary IP test value:

```text
VITE_API_BASE_URL=http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1
```

## K. Add Amplify URL to backend CORS

In server `backend/.env`, set:

```text
BACKEND_CORS_ORIGINS=https://your-amplify-domain.amplifyapp.com,https://yourdomain.com
```

Restart backend:

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

## L. Add Razorpay webhook URL

Use test mode first.

```text
https://api.yourdomain.com/api/v1/billing/webhook/razorpay
```

Keep Razorpay keys only in `backend/.env` on the server.
