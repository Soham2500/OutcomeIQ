# AWS Cost Safety Checklist

OutcomeIQ should stay inside the user’s AWS credits during early MVP validation.

## Before launch

- Enable MFA on AWS root account.
- Create an AWS Budget alert.
- Use Lightsail small instance first.
- Attach only one static IP.
- Avoid RDS unless container PostgreSQL becomes a bottleneck.
- Avoid ALB unless traffic and HTTPS needs justify it.
- Avoid NAT Gateway.
- Avoid ECS/Fargate for this early deployment.

## Weekly checks

- Review AWS Billing dashboard.
- Review Lightsail instance cost.
- Check snapshots and delete unused ones.
- Stop unused instances.
- Delete unattached static IPs.
- Check Amplify build/minute usage.

## Payment safety

- Keep `PAYMENTS_LIVE_ENABLED=false` during test deployment.
- Use Razorpay test mode first.
- Enable live payments only after HTTPS, policy pages and webhook verification.

## Upgrade only when justified

Move to RDS, ECS/Fargate or an ALB only after there is evidence of:

- real users,
- production traffic,
- reliability needs,
- database backup/restore requirements,
- clear cost approval.
