# Final Deployment Checklist - Phases 2, 3, 4
**Date:** May 27, 2026  
**Status:** Ready for Deployment  
**Estimated Time:** 15 minutes

---

## Pre-Deployment Backup

```bash
# SSH into cPanel server
cd /home3/distinc3/fagiserver.fagtone.com

# Create backup
tar -czf backup_phase2-4_$(date +%Y%m%d_%H%M%S).tar.gz fagierrandsbackup/
```

---

## Code Changes Summary

### Files Modified:
1. `fagierrandsbackup/middleware.py` - Added SafeWSGIMiddleware
2. `fagierrandsbackup/settings.py` - Added PERMISSIONS_POLICY, django.security logger, SafeWSGIMiddleware to MIDDLEWARE
3. `fagierrandsbackup/urls.py` - Added favicon redirect

### Git Commands:
```bash
# Local machine
cd /home/fagitone/Documents/GitHub/fagierrandsbackup

git add fagierrandsbackup/fagierrandsbackup/middleware.py
git add fagierrandsbackup/fagierrandsbackup/settings.py
git add fagierrandsbackup/fagierrandsbackup/urls.py

git commit -m "Phase 2-4: Add WSGI middleware, security headers, favicon redirect"

git push origin main
```

---

## Server Deployment Steps

### Step 1: Pull Latest Code
```bash
# SSH into cPanel
cd /home3/distinc3/fagiserver.fagtone.com
git pull origin main
```

### Step 2: Collect Static Files
```bash
source virtualenv/fagiserver.fagtone.com/3.11/bin/activate
python manage.py collectstatic --noinput
```

### Step 3: Add NCBA Environment Variables (cPanel)
Navigate to: **cPanel → Setup Python App → Environment Variables**

Add these variables:
```
NCBA_USERNAME = your_ncba_username
NCBA_PASSWORD = your_ncba_password
NCBA_TILL_NO = your_till_number
```

### Step 4: Restart Application
```bash
touch tmp/restart.txt
```

### Step 5: Monitor Logs
```bash
tail -f logs/stderr.log
```

---

## Post-Deployment Verification

### 1. Check Application Status
```bash
curl -I https://fagiserver.fagtone.com
# Should return 200 OK
```

### 2. Verify Security Headers
```bash
curl -I https://fagiserver.fagtone.com | grep -i "referrer-policy\|permissions-policy\|cross-origin"
```

Expected output:
```
referrer-policy: strict-origin-when-cross-origin
cross-origin-opener-policy: same-origin
permissions-policy: geolocation=(self), camera=(), microphone=()
```

### 3. Test Favicon
```bash
curl -I https://fagiserver.fagtone.com/favicon.ico
# Should return 301 or 302 redirect
```

### 4. Test Swagger UI Static Files
Visit: `https://fagiserver.fagtone.com/swagger/`
- Should load without 404 errors for CSS/JS files

### 5. Test NCBA Payment (if credentials added)
```bash
# Use your test script or Postman
# Verify no 401 errors in logs
```

### 6. Monitor Error Logs (30 minutes)
```bash
tail -f logs/stderr.log | grep -i "error\|critical\|exception"
```

Expected improvements:
- ❌ No more WSGI handler NULL errors
- ❌ No more missing static file 404s (after collectstatic)
- ❌ No more NCBA 401 errors (after credentials added)

---

## Rollback Plan (If Issues Occur)

```bash
# Stop application
touch tmp/restart.txt

# Restore backup
cd /home3/distinc3/fagiserver.fagtone.com
tar -xzf backup_phase2-4_YYYYMMDD_HHMMSS.tar.gz

# Restart
touch tmp/restart.txt
```

---

## Success Metrics

### Before Deployment:
- WSGI errors: ~30/hour
- Static file 404s: ~7,000 total
- NCBA 401 errors: 8 occurrences
- Security score: B

### After Deployment:
- WSGI errors: 0 ✅
- Static file 404s: 0 ✅
- NCBA 401 errors: 0 (with credentials) ✅
- Security score: A ✅

---

## Deployment Checklist

### Pre-Deployment
- [x] Code changes complete
- [ ] Backup created
- [ ] Git committed and pushed

### Deployment
- [ ] Code pulled on server
- [ ] `collectstatic` executed
- [ ] NCBA credentials added
- [ ] Application restarted

### Verification
- [ ] Application responds (200 OK)
- [ ] Security headers present
- [ ] Favicon redirects correctly
- [ ] Swagger UI loads completely
- [ ] No errors in logs (30 min monitoring)
- [ ] NCBA payment test successful

### Documentation
- [ ] Update team on deployment
- [ ] Document any issues encountered
- [ ] Schedule follow-up review (24 hours)

---

## Contact for Issues

**Admins:**
- dallaherick0@gmail.com
- fagierrands1@gmail.com

**Logs Location:**
- `/home3/distinc3/logs/stderr.log`

---

## Next Steps After Deployment

1. **Monitor for 24 hours**
   - Check error rates
   - Verify payment success rates
   - Monitor user registrations

2. **Frontend Fix (Phase 3.1)**
   - Notify frontend team about double `/api/` issue
   - Test after frontend deployment

3. **Optional Enhancements**
   - Add sitemap.xml (if needed for SEO)
   - Implement zero-downtime deployment
   - Add health check endpoint

---

**Deployment Ready:** ✅ Yes  
**Risk Level:** Low  
**Estimated Downtime:** < 1 minute  
**Best Time to Deploy:** Off-peak hours

---

**Prepared by:** Amazon Q  
**Date:** May 27, 2026  
**Version:** 1.0
