# Early Launch Checklist

## Technical

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] Render PostgreSQL database connected
- [ ] Migrations applied
- [ ] Plan seed applied
- [ ] Pricing seed applied
- [ ] CORS configured for the real frontend domain
- [ ] Backend health check working
- [ ] Frontend API URL correct
- [ ] Register/login working
- [ ] Demo flow working
- [ ] Dashboard working
- [ ] Recommendations working
- [ ] Pricing page working
- [ ] Billing test mode working

## Security

- [ ] `SECRET_KEY` changed from local placeholder
- [ ] `DEBUG=false`
- [ ] `.env` files not committed
- [ ] CORS limited to the real frontend domain plus required local origins
- [ ] No API keys in frontend
- [ ] No secrets in screenshots
- [ ] No secrets in README/docs
- [ ] Render and Vercel environment variables reviewed

## Legal/business before real payments

- [ ] Privacy Policy
- [ ] Terms and Conditions
- [ ] Refund/Cancellation Policy
- [ ] Contact email
- [ ] Razorpay KYC
- [ ] GST/tax advice if required
- [ ] Live webhook signature verification

## Demo

- [ ] Test account created
- [ ] Sample project created
- [ ] Demo data generated
- [ ] Screenshots captured
- [ ] Demo script prepared
- [ ] Pricing/Billing pages checked in test mode

## MVP boundary

The first live version remains simulated-provider only. Real payments and real AI provider usage are not enabled.
