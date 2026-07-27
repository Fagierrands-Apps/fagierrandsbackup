# 🔍 NCBA API - IMPORTANT CLARIFICATION

## ⚠️ NCBA Does NOT Send Webhooks!

After reviewing the official NCBA API documentation, **NCBA does not provide webhook/callback functionality**.

---

## 📋 What NCBA Actually Provides:

### ✅ **STK Push Initiate**
- Sends payment prompt to customer's phone
- Returns `TransactionID`

### ✅ **STK Push Query** (Polling)
- You call this endpoint to check payment status
- Returns: `"SUCCESS"`, `"FAILED"`, or `"PENDING"`

### ❌ **No Webhooks**
- NCBA does not call your server
- No automatic payment notifications
- No callback endpoint needed

---

## 🔄 How NCBA Payments Actually Work:

### **Step 1: Initiate Payment**
```
POST /payments/api/v1/stk-push/initiate
{
  "TelephoneNo": "254712345678",
  "Amount": "500",
  "PayBillNo": "852054",
  "AccountNo": "ORDER123",
  "Network": "Safaricom",
  "TransactionType": "CustomerPayBillOnline"
}

Response:
{
  "TransactionID": "REF123456",  ← Save this!
  "StatusCode": "0",
  "StatusDescription": "Request accepted"
}
```

### **Step 2: Poll for Status (Every 5-10 seconds)**
```
POST /payments/api/v1/stk-push/query
{
  "TransactionID": "REF123456"
}

Response (Success):
{
  "status": "SUCCESS",
  "description": "Success"
}

Response (Failed):
{
  "status": "FAILED",
  "description": "User cancelled"
}

Response (Pending):
{
  "status": "PENDING",
  "description": "Waiting for user"
}
```

### **Step 3: Update Order When SUCCESS**
- When status = "SUCCESS" → Mark order as paid
- When status = "FAILED" → Mark payment as failed
- If status = "PENDING" for >2 minutes → Timeout

---

## 🛡️ Security Implications:

### ✅ **Good News:**
- **No webhook vulnerability** (NCBA doesn't send callbacks)
- **No fake payment risk** (you're calling NCBA, not vice versa)
- Your webhook endpoint (`NCBACallbackView`) is unused

### ⚠️ **What Needs Fixing:**
- Remove or disable unused webhook endpoint
- Implement proper polling mechanism
- Add timeout handling (don't poll forever)

---

## 📝 Current Status of Your Code:

### **What Works:**
✅ STK Push initiation  
✅ Token generation  
✅ Basic payment flow

### **What's Wrong:**
❌ Webhook endpoint exists but NCBA never calls it  
❌ No polling implementation  
❌ Payment status not updated automatically  
❌ Frontend probably waits for webhook that never comes

---

## 🔧 What Needs to be Done:

### **1. Remove Webhook Endpoint (Optional)**
```python
# In urls.py, comment out or remove:
# path('payment/ncba/callback/', NCBACallbackView.as_view())
```

### **2. Implement Polling (Required)**
Use the existing `OrderPaymentStatusView` which already polls NCBA:

```python
# This endpoint already exists in your code!
GET /api/orders/payment/status/{order_id}/

# Frontend should call this every 5 seconds:
setInterval(() => {
  fetch(`/api/orders/payment/status/${orderId}/`)
    .then(response => {
      if (response.status === 'completed') {
        showSuccess();
      }
    });
}, 5000);
```

### **3. Add Celery Background Task (Better Approach)**
```python
# orders/tasks.py
from celery import shared_task
import time

@shared_task
def poll_ncba_payment(payment_id, max_attempts=24):
    """Poll NCBA payment status for 2 minutes (24 x 5 seconds)"""
    payment = Payment.objects.get(id=payment_id)
    
    for attempt in range(max_attempts):
        try:
            # Query NCBA
            result = ncba_service.stk_query(payment.mpesa_checkout_request_id)
            
            if result['status'] == 'SUCCESS':
                payment.status = 'completed'
                payment.save()
                # Update order
                order = payment.order
                order.status = 'completed'
                order.save()
                return {'status': 'success'}
            
            elif result['status'] == 'FAILED':
                payment.status = 'failed'
                payment.save()
                return {'status': 'failed'}
            
            # Still pending, wait 5 seconds
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Polling error: {e}")
    
    # Timeout after 2 minutes
    payment.status = 'timeout'
    payment.save()
    return {'status': 'timeout'}
```

---

## 📊 Comparison: Your Code vs NCBA Reality

| Feature | Your Code | NCBA Reality |
|---------|-----------|--------------|
| STK Push | ✅ Implemented | ✅ Correct |
| Webhook | ✅ Implemented | ❌ Doesn't exist |
| Polling | ⚠️ Partial (manual) | ✅ Required |
| Auto-update | ❌ Waits for webhook | ❌ Must poll |

---

## 🎯 Immediate Actions:

### **Critical (Fix Now):**
1. ✅ Understand NCBA doesn't send webhooks
2. ⏳ Implement background polling (Celery task)
3. ⏳ Update frontend to poll status endpoint

### **Optional (Nice to Have):**
1. Remove unused webhook endpoint
2. Add payment timeout handling
3. Add retry logic for failed queries

---

## 📞 No Need to Contact NCBA for:
- ❌ Webhook secret (doesn't exist)
- ❌ Webhook IP addresses (no webhooks)
- ❌ Callback configuration (not applicable)

## ✅ Your Existing Credentials Are Sufficient:
- Username: `Errand@123`
- Password: `9Y7a24B5...`
- Till Number: `852054`

---

**Bottom Line**: Your webhook endpoint is unused. Focus on implementing proper polling instead.
