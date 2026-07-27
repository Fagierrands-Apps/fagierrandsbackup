# Domain Migration Summary

**Date:** June 3, 2026  
**Old Domain:** https://errandserver.fagitone.com/  
**New Domain:** https://fagierrandsbackup.fagierrands.com/

## Changes Made

### 1. Django Settings Configuration (`fagierrandsbackup/fagierrandsbackup/settings.py`)

Updated the following configurations:

#### ALLOWED_HOSTS
- Removed: `errandserver.fagitone.com`, `www.errandserver.fagitone.com`, `fagiserver.fagtone.com`, `fagierrand.fagitone.com`
- Added: `fagierrandsbackup.fagierrands.com`

#### CSRF_TRUSTED_ORIGINS
- Removed: `https://fagierrands-server.onrender.com`, `https://errandserver.fagitone.com`, `https://www.errandserver.fagitone.com`, `https://fagiserver.fagtone.com`
- Added: `https://fagierrandsbackup.fagierrands.com`

#### CORS_ALLOWED_ORIGINS & CORS_ORIGIN_WHITELIST
- Removed: `https://errandserver.fagitone.com`, `https://www.errandserver.fagitone.com`, `https://fagiserver.fagtone.com`
- Added: `https://fagierrandsbackup.fagierrands.com`
- Kept: Vercel frontend URLs and other existing domains

#### BASE_URL (NCBA Payment Callback)
- Changed from: `https://errandserver.fagitone.com`
- Changed to: `https://fagierrandsbackup.fagierrands.com`
- This affects: `NCBA_CALLBACK_URL = f"{BASE_URL}/api/orders/payments/ncba/callback/"`

### 2. Documentation Files

Updated domain references in:
- `NCBA_QR_CODE_GUIDE.md` - Updated API endpoint examples
- `NCBA_PAYMENT_FLOW_EXPLAINED.md` - Updated API endpoint examples

## Next Steps

### 1. Update Environment Variables (cPanel)
You need to update the following environment variable in your cPanel:

```bash
BASE_URL=https://fagierrandsbackup.fagierrands.com
```

### 2. Update NCBA Payment Gateway Configuration
**CRITICAL:** You must update your NCBA webhook/callback URL in their dashboard:

- Login to NCBA Developer Portal
- Navigate to your application settings
- Update callback URL to: `https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/callback/`

### 3. SSL Certificate
Ensure your new domain has a valid SSL certificate installed in cPanel.

### 4. DNS Configuration
Verify that DNS records for `fagierrandsbackup.fagierrands.com` are properly configured to point to your server.

### 5. Test Payment Flow
After deployment, test the complete payment flow:
- STK Push initiation
- Payment callback reception
- Order status updates

### 6. Update Frontend Configuration (if needed)
If your frontend has the backend URL hardcoded, update it to the new domain:
```javascript
const API_BASE_URL = 'https://fagierrandsbackup.fagierrands.com';
```

### 7. Restart Application
After deploying changes, restart your application:
```bash
touch /home/fagitone/Documents/GitHub/fagierrandsbackup/tmp/restart.txt
```

## Files Modified

1. `/home/fagitone/Documents/GitHub/fagierrandsbackup/fagierrandsbackup/fagierrandsbackup/settings.py`
2. `/home/fagitone/Documents/GitHub/fagierrandsbackup/NCBA_QR_CODE_GUIDE.md`
3. `/home/fagitone/Documents/GitHub/fagierrandsbackup/NCBA_PAYMENT_FLOW_EXPLAINED.md`

## Testing Checklist

- [ ] Application loads at new domain
- [ ] CORS works for frontend requests
- [ ] CSRF protection works
- [ ] Payment initiation works
- [ ] NCBA callback receives webhooks
- [ ] SSL certificate is valid
- [ ] All API endpoints respond correctly

## Rollback Plan

If issues occur, you can temporarily add the old domain back to `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` while troubleshooting:

```python
ALLOWED_HOSTS = [
    'fagierrandsbackup.fagierrands.com',
    'errandserver.fagitone.com',  # Temporary
    # ...
]
```

## Notes

- The old domain references have been removed from the main configuration
- The backup settings file (`settings.py.backup`) still contains old references for historical purposes
- Environment variables provide flexibility to override defaults without code changes
