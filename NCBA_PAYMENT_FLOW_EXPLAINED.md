# NCBA Payment Flow Explanation

## Question: Will adding NCBA credentials automatically prompt users to pay?

**Short Answer:** NO - credentials alone don't trigger prompts. Your app must call the payment API.

---

## Complete Payment Flow

### Step 1: User Action (Frontend)
```
User clicks "Pay Now" button
↓
Frontend collects: phone number, amount
↓
Frontend calls YOUR backend API
```

### Step 2: Your Backend (Django)
```
POST /api/orders/payments/ncba/initiate
↓
Backend receives: phone, amount, order_id
↓
Backend calls NCBAService.initiate_stk_push()
```

### Step 3: NCBA Service (What credentials enable)
```python
# This is what happens when credentials are set:

service = NCBAService()
# Uses NCBA_USERNAME and NCBA_PASSWORD to get token
token = service.get_access_token()  

# Uses token to send STK push request
result = service.initiate_stk_push(
    phone_number="254712345678",
    amount="100",
    account_no=NCBA_TILL_NO  # Your till number
)
```

### Step 4: NCBA API
```
NCBA receives request
↓
NCBA validates till number
↓
NCBA sends STK push to user's phone
```

### Step 5: User's Phone
```
📱 M-Pesa prompt appears:
"Pay KES 100 to NCBA Till XXXXX"
[Enter PIN: ____]
[Cancel] [OK]
```

### Step 6: Callback (After user pays)
```
User enters PIN and confirms
↓
NCBA processes payment
↓
NCBA calls your callback URL
POST /api/orders/payments/ncba/callback/
↓
Your backend updates order status
```

---

## What NCBA Credentials Enable

### ✅ WITH Credentials:
```python
NCBA_USERNAME = "your_username"
NCBA_PASSWORD = "your_password"
NCBA_TILL_NO = "your_till"
```

**Enables:**
- ✅ Backend can authenticate with NCBA
- ✅ Backend can request STK push
- ✅ NCBA can send prompt to user's phone
- ✅ Payments can be processed

### ❌ WITHOUT Credentials:
```python
NCBA_USERNAME = ""  # Empty
NCBA_PASSWORD = ""  # Empty
```

**Result:**
- ❌ Backend gets 401 Unauthorized
- ❌ No STK push sent
- ❌ User sees error: "Payment failed"
- ❌ No prompt on phone

---

## Current Implementation Status

### ✅ Already Working:
1. **Backend API endpoints exist:**
   - `POST /api/orders/payments/ncba/initiate` (triggers STK)
   - `POST /api/orders/payments/ncba/callback/` (receives result)
   - `POST /api/orders/payments/ncba/qr-generate/` (QR codes)

2. **NCBA Service implemented:**
   - `NCBAService.get_access_token()` ✅
   - `NCBAService.initiate_stk_push()` ✅
   - `NCBAService.stk_query()` ✅

3. **Error handling added:**
   - Validates credentials exist
   - Better 401 error messages
   - Detailed logging

### ⚠️ Missing (What YOU need to do):
1. **Add credentials to cPanel:**
   ```
   NCBA_USERNAME=<from_your_ncba_account>
   NCBA_PASSWORD=<from_your_ncba_account>
   NCBA_TILL_NO=<your_till_number>
   ```

2. **Frontend must call the API:**
   ```javascript
   // Example frontend code (if not already done)
   fetch('/api/orders/payments/ncba/initiate', {
     method: 'POST',
     body: JSON.stringify({
       phone_number: '254712345678',
       amount: 100,
       order_id: 123
     })
   })
   ```

---

## Testing the Flow

### Test 1: Check if credentials work
```bash
# After adding credentials to cPanel, test:
python manage.py shell

from orders.ncba_service import NCBAService
service = NCBAService()

# This should work if credentials are correct:
token = service.get_access_token()
print(f"Token obtained: {token[:20]}...")
```

### Test 2: Initiate test payment
```bash
# Test STK push (use your real phone):
result = service.initiate_stk_push(
    phone_number="254712345678",  # Your phone
    amount="1",  # 1 shilling test
    account_no=service.till_no
)
print(result)

# Check your phone - you should see M-Pesa prompt!
```

### Test 3: Frontend integration
```bash
# Use Postman or curl:
curl -X POST https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/initiate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "phone_number": "254712345678",
    "amount": "1",
    "order_id": 123
  }'
```

---

## Common Issues

### Issue 1: "No prompt on phone"
**Cause:** Credentials not set or incorrect
**Fix:** Verify NCBA_USERNAME, NCBA_PASSWORD in cPanel

### Issue 2: "401 Unauthorized"
**Cause:** Wrong username/password
**Fix:** Double-check credentials from NCBA

### Issue 3: "Payment initiated but no callback"
**Cause:** Callback URL not registered with NCBA
**Fix:** Contact NCBA to register:
```
https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/callback/
```

### Issue 4: "Invalid till number"
**Cause:** Wrong NCBA_TILL_NO
**Fix:** Use the till number from your NCBA account

---

## Summary

### What Credentials Do:
✅ Enable backend to talk to NCBA API  
✅ Allow STK push requests to be sent  
✅ Authenticate your application  

### What Credentials DON'T Do:
❌ Don't automatically prompt users  
❌ Don't replace frontend payment button  
❌ Don't bypass your backend API  

### What Triggers the Prompt:
1. User clicks "Pay" in your app
2. Frontend calls your backend API
3. Backend calls NCBA with credentials
4. NCBA sends STK push to user's phone
5. User sees prompt and enters PIN

---

## Next Steps

1. **Add credentials to cPanel** (required)
2. **Deploy Phase 1 fixes** (1.1 + 1.2 + 1.3)
3. **Test with 1 shilling payment** (your phone)
4. **Verify callback receives payment status**
5. **Test full order flow** (create order → pay → confirm)

---

**Bottom Line:** Credentials are necessary but not sufficient. Your app must actively call the NCBA API to trigger payment prompts.
