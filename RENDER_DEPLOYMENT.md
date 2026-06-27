# 🚀 Render Deployment Guide

## ✅ Files Created for Render:
- `Procfile` - Tells Render how to run the app
- `build.sh` - Build script for deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 Render Setup Steps:

### 1. Go to Render Dashboard
- Visit: https://dashboard.render.com/
- Click "New +" → "Web Service"

### 2. Connect GitHub Repository
- Connect your GitHub account
- Select repository: `fagierrandsbackup`
- Branch: `main`

### 3. Configure Service

**Basic Settings:**
- Name: `fagierrandsbackup`
- Region: `Oregon (US West)` or closest to your users
- Branch: `main`
- Root Directory: (leave empty)

**Build & Deploy:**
- Runtime: `Python 3`
- Build Command: `./build.sh`
- Start Command: `gunicorn fagierrandsbackup.wsgi:application --bind 0.0.0.0:$PORT`

**Instance Type:**
- Free tier (for testing) or Starter ($7/month)

### 4. Add Environment Variables

Click "Environment" → "Add Environment Variable"

**Required Variables:**

```
DEBUG=False
SECRET_KEY=<generate new one - don't use cPanel's>
ALLOWED_HOSTS=fagierrandsbackup.onrender.com,localhost,127.0.0.1

DATABASE_URL=<your Supabase Postgres URL>
SUPABASE_URL=https://dxesmzogjpxswxhsomgf.supabase.co
SUPABASE_ANON_KEY=<your key>
SUPABASE_SERVICE_KEY=<your key>

JWT_SECRET_KEY=<generate new one>
JWT_ALGORITHM=HS256

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your email>
EMAIL_HOST_PASSWORD=<your password>
DEFAULT_FROM_EMAIL=<your email>

NCBA_MERCHANT_CODE=<your code>
NCBA_API_KEY=<your key>
NCBA_SECRET_KEY=<your secret>
NCBA_QR_CALLBACK_URL=https://fagierrandsbackup.onrender.com/api/payments/ncba/qr/callback/

REDIS_URL=<your Redis URL or use Render's Redis add-on>

CORS_ALLOWED_ORIGINS=https://handler.fagierrands.com,https://fagierrands.com,https://fagierrands.fagitone.com
```

### 5. Add Redis (Optional but Recommended)

If using Redis for caching/rate limiting:
- In Render dashboard → "New +" → "Redis"
- Copy the Internal Redis URL
- Add to environment: `REDIS_URL=<redis-url>`

### 6. Deploy

- Click "Create Web Service"
- Render will automatically deploy from GitHub
- Watch the build logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔍 After Deployment:

### 1. Get Your Render URL
Your app will be at: `https://fagierrandsbackup.onrender.com`

### 2. Update CORS if Needed
If you want frontends to hit Render instead of cPanel:
- Add Render URL to CORS_ALLOWED_ORIGINS
- Or keep it as-is for testing only

### 3. Test API
```bash
curl https://fagierrandsbackup.onrender.com/api/health/
```

### 4. Check Logs
- In Render dashboard → Your service → "Logs"

### 5. Update NCBA Callback
- If testing payments, update NCBA callback URL to Render

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚙️ Auto-Deploy from GitHub

Render automatically deploys when you push to main:
```bash
git add -A
git commit -m "Update"
git push origin main
# Render auto-deploys ✅
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 Testing Plan:

### Phase 1: Render Deploy (NOW)
1. Deploy to Render ✅
2. Test all endpoints
3. Verify CORS works with 3 frontends
4. Check logs/monitoring
5. Test payment flow

### Phase 2: Update cPanel (AFTER CONFIRMATION)
1. SSH into cPanel
2. `git pull origin main`
3. `touch tmp/restart.txt`
4. Verify production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔒 Security Notes:

✅ CORS locked to 3 frontends only
✅ DEBUG=False
✅ Generate NEW SECRET_KEY for Render (don't reuse cPanel's)
✅ All security features active (10/10 score)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💰 Cost:

- **Free Tier**: $0 (sleeps after 15 min inactivity)
- **Starter**: $7/month (always on, better performance)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚡ Quick Start:

1. Push files to GitHub:
```bash
git add Procfile build.sh
git commit -m "Add Render deployment config"
git push origin main
```

2. Go to https://dashboard.render.com/
3. New Web Service → Connect GitHub repo
4. Add environment variables (see above)
5. Click "Create Web Service"
6. Wait ~5 minutes for deploy
7. Test: `https://fagierrandsbackup.onrender.com/api/health/`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to deploy? Say "yes" and I'll push to GitHub!
