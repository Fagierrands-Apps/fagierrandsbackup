# Phase 1.2: Remove M-Pesa + Fix NCBA STK Push

**Date:** May 27, 2026 09:42 AM  
**Status:** READY TO EXECUTE  
**Priority:** CRITICAL (P0)

---

## OBJECTIVES

1. ✅ Remove ALL M-Pesa code and dependencies
2. ✅ Keep ONLY NCBA STK Push implementation
3. ✅ Fix NCBA 401 authentication errors (8 occurrences in logs)
4. ✅ Simplify payment flow to single provider
5. ✅ Update settings to use safe `.get()` methods

---

## NCBA API DOCUMENTATION SUMMARY

### Base URL
```
https://c2bapis.ncbagroup.com
```

### Authentication Flow
1. **Get Token:** `GET /payments/api/v1/auth/token`
   - Method: Basic Auth (username:password)
   - Returns: JWT access_token (expires in 18000 seconds = 5 hours)
   - Cache token to avoid repeated calls

2. **Initiate STK Push:** `POST /payments/api/v1/stk-push/initiate`
   - Authorization: Bearer {access_token}
   - Payload:
     ```json
     {
       "TelephoneNo": "254XXXXXXXX",
       "Amount": "100",
       "PayBillNo": "880100",
       "AccountNo": "TILL_NUMBER",
       "Network": "Safaricom",
       "TransactionType": "CustomerPayBillOnline"
     }
     ```

3. **Query Status:** `POST /payments/api/v1/stk-push/query`
   - Check transaction status using TransactionID

### Required Environment Variables
```bash
NCBA_USERNAME=<your_username>
NCBA_PASSWORD=<your_password>
NCBA_PAYBILL_NO=880100
NCBA_TILL_NO=<your_till_number>
```

---

## FILES TO MODIFY

### 1. Settings (fagierrandsbackup/settings.py)

**REMOVE (Lines ~450-460):**
```python
# Legacy M-Pesa settings
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'production')
MPESA_CONSUMER_KEY = os.environ['MPESA_CONSUMER_KEY']  # ❌ CRASHES
MPESA_CONSUMER_SECRET = os.environ['MPESA_CONSUMER_SECRET']
MPESA_SHORTCODE = os.environ['MPESA_SHORTCODE']
MPESA_PASSKEY = os.environ['MPESA_PASSKEY']
MPESA_PARTYB_SHORTCODE = os.environ['MPESA_PARTYB_SHORTCODE']

# Legacy M-Pesa Callback URLs
MPESA_STK_CALLBACK_URL = f"{BASE_URL}/api/orders/payments/mpesa/stk-callback/"
MPESA_C2B_VALIDATION_URL = f"{BASE_URL}/api/orders/payments/mpesa/c2b-validation/"
MPESA_C2B_CONFIRMATION_URL = f"{BASE_URL}/api/orders/payments/mpesa/c2b-confirmation/"
MPESA_B2C_RESULT_URL = f"{BASE_URL}/api/orders/payments/mpesa/b2c-result/"
MPESA_B2C_TIMEOUT_URL = f"{BASE_URL}/api/orders/payments/mpesa/b2c-timeout/"
```

**KEEP & FIX (NCBA settings):**
```python
# NCBA Till API settings (ONLY payment provider)
NCBA_USERNAME = os.environ.get('NCBA_USERNAME', '')
NCBA_PASSWORD = os.environ.get('NCBA_PASSWORD', '')
NCBA_PAYBILL_NO = os.environ.get('NCBA_PAYBILL_NO', '880100')
NCBA_TILL_NO = os.environ.get('NCBA_TILL_NO', '')
NCBA_TRANSACTION_TYPE = os.environ.get('NCBA_TRANSACTION_TYPE', 'CustomerPayBillOnline')
NCBA_USE_TILL_AS_ACCOUNT = os.environ.get('NCBA_USE_TILL_AS_ACCOUNT', 'False').upper() == 'TRUE'
NCBA_CALLBACK_URL = f"{BASE_URL}/api/orders/payments/ncba/callback/"
```

---

### 2. Files to DELETE (Move to archive)

```bash
# Test files (not needed in production)
./diagnose_mpesa_config.py
./test_django_mpesa.py
./test_mpesa_live.py
./run_mpesa_tests.bat
./test_mpesa_integration.py
./test_mpesa_comprehensive.py
./run_mpesa_tests.ps1
./quick_test_mpesa.py
./test_mpesa_simple.py

# Service files
./orders/views_payment_mpesa.py
./orders/mpesa_service.py
./orders/management/commands/test_mpesa_stk.py
```

---

### 3. NCBA Service Fix (orders/ncba_service.py)

**Current Issue:** 401 authentication errors

**Root Cause Analysis:**
- Username/password not set in cPanel environment
- Basic Auth encoding might be incorrect
- Token caching might be stale

**Fix Required:**
```python
def get_access_token(self):
    """Enhanced with better error handling"""
    cache_key = 'ncba_access_token'
    token = cache.get(cache_key)
    
    if token:
        logger.info("Using cached NCBA access token")
        return token
    
    # Validate credentials exist
    if not self.username or not self.password:
        raise Exception("NCBA credentials not configured. Set NCBA_USERNAME and NCBA_PASSWORD in environment.")
    
    try:
        url = f"{self.base_url}/payments/api/v1/auth/token"
        logger.info(f"Fetching NCBA access token for user: {self.username}")
        
        # Basic Auth (username:password)
        auth_string = f"{self.username}:{self.password}"
        auth_bytes = auth_string.encode('ascii')
        auth_base64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=self.timeout)
        
        # Log response for debugging
        logger.info(f"NCBA auth response status: {response.status_code}")
        
        if response.status_code == 401:
            logger.error(f"NCBA 401 Unauthorized - Check credentials")
            logger.error(f"Username: {self.username}")
            logger.error(f"Response: {response.text}")
            raise Exception("Invalid NCBA credentials - verify NCBA_USERNAME and NCBA_PASSWORD")
        
        response.raise_for_status()
        
        result = response.json()
        token = result.get('access_token')
        expires_in = result.get('expires_in', 18000)
        
        if token:
            logger.info("NCBA access token obtained successfully")
            # Cache for 4.5 hours (18000 - 900 seconds buffer)
            cache.set(cache_key, token, expires_in - 900)
            return token
        else:
            raise Exception("No access token in NCBA response")
            
    except Exception as e:
        logger.error(f"NCBA authentication failed: {str(e)}")
        raise
```

---

### 4. Database Migrations (Keep but don't use)

**Keep these files** (for historical data):
```
./orders/migrations/0029_payment_mpesa_transaction_id.py
./orders/migrations/0025_migrate_to_mpesa_daraja.py
./orders/migrations/0030_ensure_mpesa_columns_exist.py
./orders/migrations/0028_add_mpesa_transaction_id.py
```

**Reason:** Old payments might have M-Pesa transaction IDs. Don't break existing data.

---

## EXECUTION STEPS

### Step 1: Update Settings
```bash
# Edit fagierrandsbackup/settings.py
# Remove lines 450-460 (M-Pesa settings)
# Keep NCBA settings with .get() methods
```

### Step 2: Archive M-Pesa Files
```bash
mkdir -p archive/mpesa_removed_2026_05_27
mv diagnose_mpesa_config.py archive/mpesa_removed_2026_05_27/
mv test_*mpesa*.py archive/mpesa_removed_2026_05_27/
mv run_mpesa_tests.* archive/mpesa_removed_2026_05_27/
mv quick_test_mpesa.py archive/mpesa_removed_2026_05_27/
mv orders/views_payment_mpesa.py archive/mpesa_removed_2026_05_27/
mv orders/mpesa_service.py archive/mpesa_removed_2026_05_27/
mv orders/management/commands/test_mpesa_stk.py archive/mpesa_removed_2026_05_27/
```

### Step 3: Fix NCBA Service
```bash
# Update orders/ncba_service.py
# Add credential validation
# Improve error messages
# Add detailed logging
```

### Step 4: Update cPanel Environment Variables
```bash
# Add these in cPanel Environment Variables table:
NCBA_USERNAME=<from_your_ncba_account>
NCBA_PASSWORD=<from_your_ncba_account>
NCBA_PAYBILL_NO=880100
NCBA_TILL_NO=<your_till_number>
```

### Step 5: Test Locally
```bash
python manage.py shell
from orders.ncba_service import NCBAService
service = NCBAService()
token = service.get_access_token()
print(f"Token: {token[:20]}...")
```

---

## EXPECTED IMPACT

### Before:
- ❌ 23 KeyError crashes (M-Pesa env vars missing)
- ❌ 8 NCBA 401 authentication errors
- ❌ Confusing dual payment system
- ❌ Unused M-Pesa code bloat

### After:
- ✅ Zero M-Pesa related crashes
- ✅ NCBA authentication works
- ✅ Single, simple payment flow
- ✅ Cleaner codebase

---

## TESTING CHECKLIST

- [ ] Settings file has no M-Pesa references
- [ ] NCBA credentials set in cPanel
- [ ] NCBA token generation works
- [ ] STK push initiates successfully
- [ ] Payment callback received
- [ ] No import errors
- [ ] Application starts without crashes

---

## ROLLBACK PLAN

```bash
# Restore from archive
cp archive/mpesa_removed_2026_05_27/* .

# Restore settings
git checkout HEAD~1 fagierrandsbackup/settings.py

# Restart
touch tmp/restart.txt
```

---

## NEXT STEPS AFTER COMPLETION

1. Deploy Phase 1.1 + 1.2 together
2. Proceed to Phase 1.3 (Email authentication fix)
3. Test complete payment flow end-to-end
4. Monitor logs for 1 hour

---

**Status:** READY TO EXECUTE  
**Estimated Time:** 30 minutes  
**Risk Level:** MEDIUM (payment system changes)  
**Requires Testing:** YES (critical payment flow)
