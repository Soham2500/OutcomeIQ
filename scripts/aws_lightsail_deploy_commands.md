# AWS Lightsail Manual Deploy Commands

These commands are for the Ubuntu Lightsail instance. Replace placeholders manually. Do not paste secrets into Git or chat.

## 1. SSH into Lightsail

```bash
ssh ubuntu@YOUR_LIGHTSAIL_STATIC_IP
```

## 2. Run server setup once

```bash
cd /tmp
# Upload or copy scripts/aws_lightsail_server_setup.sh first.
bash aws_lightsail_server_setup.sh
```

Log out and SSH back in after Docker group membership is updated.

## 3. Clone the repository

```bash
cd /opt/outcomeiq
git clone https://github.com/Soham2500/OutcomeIQ.git .
```

## 4. Create private backend environment file

```bash
cp backend/.env.aws.example backend/.env
nano backend/.env
```

Replace placeholders only on the server. Never commit `backend/.env`.

## 5. Start backend and PostgreSQL

```bash
docker compose -f docker-compose.aws.yml up -d --build
```

## 6. Check containers and logs

```bash
docker compose -f docker-compose.aws.yml ps
docker compose -f docker-compose.aws.yml logs -f backend
```

## 7. Run migrations

```bash
docker compose -f docker-compose.aws.yml exec backend alembic upgrade head
```

## 8. Seed plans/pricing if needed

Use existing backend scripts only after reviewing them. For local project-root PowerShell helpers, run equivalent commands inside the backend container when needed.

```bash
docker compose -f docker-compose.aws.yml exec backend python -m scripts.seed_plans
```

If that module is unavailable, seed through the existing documented local process before relying on Pricing.

## 9. Health check

```bash
curl http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1/health
curl http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1/ready
```

## 10. Restart after env changes

```bash
docker compose -f docker-compose.aws.yml up -d --build
```
