# 🔐 NCBA Webhook Security - Simple Explanation

## ❓ What's the Difference?

### **Credentials You Already Have:**

```
NCBA_USERNAME = Errand@123
NCBA_PASSWORD = 9Y7a24B5...
NCBA_TILL_NO = 852054
```

**Used for**: When YOUR server talks TO NCBA  
**Example**: "Hey NCBA, initiate payment for Order #123"

---

### **What Was Missing: Webhook Protection**

**Used for**: When NCBA talks TO YOUR server  
**Example**: "Hey Fagi Errands, payment for Order #123 is complete"

**Problem**: Anyone could fake this message!

---

## ⚠️ The Security Risk (Before Fix):

**Hacker could do this:**
```bash
curl -X POST https://fagierrandsbackup.fagierrands.com/api/orders/payment/ncba/callback/ \
  -d '{"order_id": 123, "status": "SUCCESS"}'
```

**Result**: Order #123 marked as PAID (without actually paying!) 💸💸💸

---

## ✅ The Fix (IP Whitelisting):

**Now your server checks:**
1. Is this webhook from NCBA's IP address? 
2. If YES → Process payment ✅
3. If NO → Reject it ❌

**Code Added:**
```python
NCBA_WHITELISTED_IPS = []  # Add NCBA's IPs here

if client_ip not in NCBA_WHITELISTED_IPS:
    return Response({'error': 'Unauthorized'}, status=403)
```

---

## 📋 What You Need to Do:

### **Contact NCBA and Ask:**

> "What IP addresses do your webhook/callback requests come from? We need to whitelist them for security."

**They might give you something like:**
- `41.90.174.25`
- `197.232.15.100`

### **Then Update the Code:**

**File:** `orders/views_payment_ncba.py` (line ~471)

```python
NCBA_WHITELISTED_IPS = [
    '41.90.174.25',      # Replace with actual NCBA IP
    '197.232.15.100',    # Replace with actual NCBA IP
]
```

---

## 🎯 Current Status:

✅ **IP whitelisting code added**  
✅ **All webhooks logged** (you can monitor)  
⏳ **Need NCBA IPs** (contact NCBA support)  
⏳ **Whitelist is empty** (currently logs but allows all)

**Until you add NCBA IPs:**
- Webhooks are logged ✅
- But not blocked yet ⚠️
- Still vulnerable to fake payments ⚠️

---

## 🔍 How to Monitor:

**Check logs to see webhook IPs:**
```bash
# Look for lines like:
"NCBA webhook from IP: 41.90.x.x"
```

**Once you see real NCBA webhooks, add those IPs to the whitelist!**

---

## ✅ Summary:

| Item | What It's For | You Have It? |
|------|---------------|--------------|
| NCBA_USERNAME | You → NCBA requests | ✅ Yes |
| NCBA_PASSWORD | You → NCBA requests | ✅ Yes |
| NCBA_TILL_NO | Your till number | ✅ Yes |
| **IP Whitelist** | NCBA → You webhooks | ⏳ Need IPs from NCBA |

---

**Next Step**: Call NCBA support and ask for their webhook IP addresses! 📞
