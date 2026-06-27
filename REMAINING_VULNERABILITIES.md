# 🚨 Remaining Security Vulnerabilities

## Critical Issues Still Unfixed:

### 1. **File Upload Validation** ⚠️ HIGH RISK

**Location**: `accounts/storage_utils.py`

**Problem**: No validation on uploaded files
```python
def upload_verification_image(file, user_id, file_type='verification'):
    # ❌ Accepts ANY file type (.exe, .php, .sh)
    # ❌ No size limit check
    # ❌ No content validation
    file_extension = os.path.splitext(file.name)[1]
    filename = f"{user_id}_{file_type}_{file.name}"
```

**What Could Happen**:
- User uploads malicious `.php` file
- File gets executed on server
- Hacker gains server access
- Database compromised

**How to Exploit**:
```bash
# Attacker uploads malicious file
curl -X POST /api/accounts/profile/update/ \
  -F "national_id_front=@malware.php.jpg"
```

**Fix Required**: ✅ Add file type & size validation

---

### 2. **Order Price Manipulation** ⚠️ MEDIUM-HIGH RISK

**Location**: `orders/views.py` - Order creation

**Problem**: Client can send any price
```python
# Frontend sends:
{
  "order_type": "delivery",
  "distance": 10,
  "price": 50  ← Client controls this!
}

# Server saves it without validation ❌
```

**What Could Happen**:
- User creates 50km delivery order
- Should cost: KSh 1200
- User sends: `"price": 10`
- Order created for KSh 10
- You lose KSh 1190 per order

**How to Exploit**:
```javascript
// Modified mobile app or API call
fetch('/api/orders/create/', {
  method: 'POST',
  body: JSON.stringify({
    ...orderData,
    price: 1  // Pay KSh 1 for any order
  })
})
```

**Fix Required**: ✅ Validate price server-side

---

### 3. **Weak Password Policy** ⚠️ MEDIUM RISK

**Location**: `fagierrandsbackup/settings.py`

**Problem**: Passwords can be simple
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': '...MinimumLengthValidator'},  # Only checks length
    # ❌ No complexity check
]
```

**What Could Happen**:
- Users set passwords: `password123`, `12345678`
- Accounts easily brute-forced
- Payment details stolen
- Orders placed fraudulently

**Current Status**: Validator created but not enabled

**Fix Required**: ✅ Enable password complexity validator

---

### 4. **No JWT Token Blacklisting** ⚠️ MEDIUM RISK

**Problem**: Logout doesn't invalidate tokens
```python
# User logs out → Token still valid for 60 minutes!
```

**What Could Happen**:
- User's phone stolen
- Thief can't login (password protected)
- But old JWT token in app storage still works
- Thief places orders, sees history, changes profile

**Scenario**:
```
1. User logs in → Gets token (valid 60 min)
2. User's phone stolen after 10 min
3. User logs out remotely
4. Token still works for 50 more minutes! ❌
5. Thief uses app normally
```

**Fix Required**: ✅ Implement token blacklisting

---

### 5. **No Rate Limiting on Login** ⚠️ MEDIUM RISK

**Location**: `fagierrandsbackup/middleware.py`

**Problem**: Same rate limit for all endpoints
```python
self.max_requests = 100  # per minute for EVERYTHING
```

**What Could Happen**:
- Attacker tries 100 passwords in 1 minute
- After 1 minute, tries 100 more
- Eventually guesses password
- Account compromised

**Brute Force Example**:
```python
passwords = ['password123', 'admin123', '12345678', ...]
for pwd in passwords[:100]:  # 100 attempts/minute allowed
    try_login(username, pwd)
```

**Fix Required**: ✅ Stricter limits for auth endpoints (5/min)

---

### 6. **SQL Injection via Raw Queries** ⚠️ LOW RISK (But Check)

Let me scan for raw SQL:
