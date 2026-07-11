# AWS Amplify Frontend Guide

OutcomeIQ’s frontend is a React/Vite app and can be hosted on AWS Amplify.

## Connect repository

1. Open AWS Amplify Hosting.
2. Connect GitHub.
3. Select the OutcomeIQ repository.
4. Set app root:

```text
frontend
```

## Build settings

Amplify config file:

```text
frontend/amplify.yml
```

Build command:

```text
npm run build
```

Output directory:

```text
dist
```

## Environment variable

Set:

```text
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

Temporary IP-based backend testing:

```text
VITE_API_BASE_URL=http://YOUR_LIGHTSAIL_STATIC_IP:8000/api/v1
```

Do not put backend secrets, Razorpay secrets or AWS access keys in Amplify frontend variables.

## SPA rewrite

If direct routes like `/dashboard` or `/pricing` return 404, add an Amplify rewrite rule:

```text
Source address: </^[^.]+$|\.(?!(css|gif|ico|jpg|js|png|txt|svg|woff|woff2)$)([^.]+$)/>
Target address: /index.html
Type: 200 (Rewrite)
```

## Redeploy process

1. Push code to GitHub.
2. Amplify rebuilds automatically.
3. Confirm frontend loads.
4. Run browser smoke tests.
5. Run AWS live smoke from local machine.
