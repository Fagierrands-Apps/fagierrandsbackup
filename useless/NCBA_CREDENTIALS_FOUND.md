# 🔑 NCBA CREDENTIALS FOUND

**Source:** `~/Downloads/fagierrands-main/fagierrands/fagierrandsbackup/quick_test_ncba.py`

---

## NCBA API Credentials

### Add These to cPanel Environment Variables:

```bash
NCBA_USERNAME=Errand@123

NCBA_PASSWORD=9Y7a24B5TNxxKimfnGz9MTbdn960JY57ASC/r6KOCQNnR220v52od6a2ajgEaipL

NCBA_TILL_NO=852054
```

---

## Optional (Already Have Defaults):

```bash
NCBA_PAYBILL_NO=880100
```

---

## How to Add to cPanel:

### Step 1: Login to cPanel
- Go to your cPanel URL
- Login with credentials

### Step 2: Navigate to Environment Variables
- Search for "Environment Variables"
- Or find under "Software" section

### Step 3: Add Variables

**Variable 1:**
```
Name: NCBA_USERNAME
Value: Errand@123
```
Click "Add Variable"

**Variable 2:**
```
Name: NCBA_PASSWORD
Value: 9Y7a24B5TNxxKimfnGz9MTbdn960JY57ASC/r6KOCQNnR220v52od6a2ajgEaipL
```
Click "Add Variable"

**Variable 3:**
```
Name: NCBA_TILL_NO
Value: 852054
```
Click "Add Variable"

---

## Verification After Adding:

### Test on Server:
```bash
cd /home3/distinc3/fagiserver.fagtone.com
source virtualenv/fagiserver.fagtone.com/3.11/bin/activate

python manage.py shell
```

```python
from orders.ncba_service import NCBAService
service = NCBAService()

# Check credentials loaded
print(f"Username: {service.username}")
print(f"Till: {service.till_no}")

# Test authentication
token = service.get_access_token()
print(f"✅ Token obtained: {token[:20]}...")
```

**Expected Output:**
```
Username: Errand@123
Till: 852054
✅ Token obtained: eyJhbGciOiJIUzI1NiIs...
```

---

## Summary

**Found Credentials:**
- ✅ NCBA_USERNAME: `Errand@123`
- ✅ NCBA_PASSWORD: `9Y7a24B5TNxxKimfnGz9MTbdn960JY57ASC/r6KOCQNnR220v52od6a2ajgEaipL`
- ✅ NCBA_TILL_NO: `852054`

**Next Steps:**
1. Add these 3 variables to cPanel
2. Add Brevo email credentials
3. Restart application
4. Test payment flow

---

**⚠️ SECURITY NOTE:**
These credentials are for your NCBA Till API. Keep them secure and only add to cPanel environment variables (not in code).
