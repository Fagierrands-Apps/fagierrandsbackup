# Quick Reference - Domain Migration

## 🔄 Domain Change
```
OLD: https://errandserver.fagitone.com/
NEW: https://fagierrandsbackup.fagierrands.com/
```

## ✅ Files Updated
1. `fagierrandsbackup/fagierrandsbackup/settings.py` - Main configuration
2. `NCBA_PAYMENT_FLOW_EXPLAINED.md` - Documentation
3. `NCBA_QR_CODE_GUIDE.md` - Documentation  
4. `PHASE_1.3_COMPLETE.md` - Documentation
5. `static/robots.txt` - SEO configuration

## 🚀 Immediate Actions Required

### 1. Update cPanel Environment Variable
```bash
BASE_URL=https://fagierrandsbackup.fagierrands.com
```

### 2. Update NCBA Dashboard
Register new callback URL with NCBA:
```
https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/callback/
```

### 3. Deploy Changes
```bash
# From project root
git add .
git commit -m "Update server domain to fagierrandsbackup.fagierrands.com"
git push origin main

# Restart application (cPanel)
touch tmp/restart.txt
```

## 🧪 Testing URLs

### Health Check
```bash
curl https://fagierrandsbackup.fagierrands.com/
```

### API Documentation
```
https://fagierrandsbackup.fagierrands.com/api/docs/
https://fagierrandsbackup.fagierrands.com/swagger/
```

### Test Payment Initiation
```bash
curl -X POST https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/initiate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "order_id": "test-order-123",
    "amount": 10,
    "phone_number": "254712345678"
  }'
```

## 📋 Testing Checklist
- [ ] Application loads at new domain
- [ ] SSL certificate is valid (green padlock)
- [ ] Admin panel accessible: `/admin/`
- [ ] API docs accessible: `/api/docs/`
- [ ] CORS works from frontend
- [ ] Payment initiation works
- [ ] NCBA callback receives webhooks
- [ ] Order creation and updates work

## 🔧 Configuration Changes Made

### ALLOWED_HOSTS
Now includes: `fagierrandsbackup.fagierrands.com`

### CSRF_TRUSTED_ORIGINS
Now includes: `https://fagierrandsbackup.fagierrands.com`

### CORS_ALLOWED_ORIGINS
Now includes: `https://fagierrandsbackup.fagierrands.com`

### BASE_URL (Default)
Changed to: `https://fagierrandsbackup.fagierrands.com`

### NCBA_CALLBACK_URL
Now points to: `https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/callback/`

## ⚠️ Critical Notes

1. **NCBA Callback:** Must be updated in NCBA dashboard or payments will fail
2. **Environment Variable:** BASE_URL must be set in cPanel to override default
3. **DNS:** Ensure domain points to your server IP
4. **SSL:** Ensure SSL certificate is installed for new domain
5. **Frontend:** Update frontend API base URL if hardcoded

## 🆘 Rollback (if needed)

If issues occur, you can temporarily restore old domain:

```python
# In settings.py ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'fagierrandsbackup.fagierrands.com',
    'errandserver.fagitone.com',  # Temporary fallback
    # ...
]
```

## 📞 Support Contacts
- Admin Emails: dallaherick0@gmail.com, fagierrands1@gmail.com
- NCBA Support: Contact for callback URL registration

---
**Created:** June 3, 2026  
**Status:** Ready for deployment
