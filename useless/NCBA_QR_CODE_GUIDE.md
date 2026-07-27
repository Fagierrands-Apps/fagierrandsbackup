# NCBA QR Code Payment Guide

## Yes! QR Code Generation is Available

From NCBA documentation: **Section 2 - QR CODE**

---

## What You Already Have ✅

### 1. Backend Implementation
**File:** `orders/ncba_service.py`
```python
def generate_qr(self, amount=None, narration=None):
    """Generate payment QR code"""
    # Returns Base64 QR code image
```

### 2. API Endpoint
**URL:** `POST /api/orders/payments/ncba/qr-generate/`
```json
// Request:
{
  "amount": 100,
  "order_id": 123
}

// Response:
{
  "StatusDescription": "Success",
  "Base64QrCode": "data:image/png;base64,iVBORw0KGgo...",
  "StatusCode": "0"
}
```

---

## How QR Codes Help Your Business

### Use Case 1: Checkout Page Alternative
**Problem:** User doesn't want to share phone number  
**Solution:** Show QR code option

```javascript
// Frontend implementation
function showQRPayment(orderId, amount) {
  fetch('/api/orders/payments/ncba/qr-generate/', {
    method: 'POST',
    body: JSON.stringify({
      amount: amount,
      order_id: orderId
    })
  })
  .then(res => res.json())
  .then(data => {
    // Display QR code
    document.getElementById('qr-image').src = data.Base64QrCode;
    document.getElementById('qr-modal').show();
  });
}
```

**User Experience:**
```
Checkout Page
├─ Option 1: Pay via Phone (STK Push)
│  └─ Enter phone → Receive prompt
│
└─ Option 2: Pay via QR Code
   └─ Scan QR → Pay in M-Pesa app
```

---

### Use Case 2: Invoice/Receipt QR
**Problem:** Customer needs to pay later  
**Solution:** Email invoice with QR code

```python
# Generate QR for order
from orders.ncba_service import NCBAService

service = NCBAService()
qr_data = service.generate_qr(
    amount=order.total_amount,
    narration=f"Order#{order.id}"
)

# Email to customer
send_invoice_email(
    customer=order.customer,
    qr_code=qr_data['Base64QrCode'],
    amount=order.total_amount
)
```

**Benefits:**
- Customer pays at convenience
- No phone number needed
- Clear payment reference
- Professional invoicing

---

### Use Case 3: In-Person Payments
**Problem:** Customer at your office/shop  
**Solution:** Display QR on screen

```python
# Generate QR for walk-in customer
qr_data = service.generate_qr(
    amount=500,
    narration="Walk-in Payment"
)

# Display on screen or print
print_qr_code(qr_data['Base64QrCode'])
```

**Flow:**
```
Customer arrives
↓
Staff generates QR
↓
Display on screen/tablet
↓
Customer scans with M-Pesa
↓
Payment received instantly
```

---

### Use Case 4: Fixed Amount QR (Reusable)
**Problem:** Same service, same price  
**Solution:** Generate once, use many times

```python
# Generate QR for standard service
qr_data = service.generate_qr(
    amount=1000,  # Fixed price
    narration="Standard Service"
)

# Print on business card or flyer
# Customer can scan anytime
```

**Examples:**
- Consultation fee: KES 500
- Delivery fee: KES 200
- Membership: KES 1000/month

---

### Use Case 5: Dynamic Amount QR
**Problem:** Amount varies per customer  
**Solution:** Generate without amount

```python
# Generate QR without fixed amount
qr_data = service.generate_qr(
    amount=None,  # Customer enters amount
    narration="Fagi Errands Payment"
)
```

**User Experience:**
```
Customer scans QR
↓
M-Pesa asks: "Enter amount"
↓
Customer types amount
↓
Customer enters PIN
↓
Payment complete
```

---

## QR Code vs STK Push Comparison

| Feature | STK Push | QR Code |
|---------|----------|---------|
| **Phone number needed** | Yes ✅ | No ❌ |
| **Internet required** | Yes (both sides) | Only for generation |
| **User control** | Backend initiates | User initiates |
| **Printed materials** | No ❌ | Yes ✅ |
| **Reusable** | No ❌ | Yes ✅ |
| **Speed** | Fast (auto-prompt) | Medium (scan + confirm) |
| **Privacy** | Less (shares phone) | More (no phone needed) |
| **Best for** | Online checkout | Invoices, in-person |

---

## Implementation Examples

### Example 1: Add QR Option to Checkout

**Frontend (React/Vue):**
```javascript
<div class="payment-options">
  <button @click="payViaPhone">
    📱 Pay via Phone (STK Push)
  </button>
  
  <button @click="payViaQR">
    📷 Pay via QR Code
  </button>
</div>

<div v-if="showQR" class="qr-modal">
  <h3>Scan to Pay KES {{ amount }}</h3>
  <img :src="qrCode" alt="Payment QR Code" />
  <p>Open M-Pesa app and scan this code</p>
</div>

<script>
methods: {
  async payViaQR() {
    const response = await fetch('/api/orders/payments/ncba/qr-generate/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: this.order.total,
        order_id: this.order.id
      })
    });
    
    const data = await response.json();
    this.qrCode = data.Base64QrCode;
    this.showQR = true;
  }
}
</script>
```

---

### Example 2: Email Invoice with QR

**Backend (Django):**
```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import base64

def send_invoice_with_qr(order):
    # Generate QR
    service = NCBAService()
    qr_data = service.generate_qr(
        amount=order.total_amount,
        narration=f"Invoice-{order.invoice_number}"
    )
    
    # Extract base64 image
    qr_image = qr_data['Base64QrCode']
    
    # Render email template
    html_content = render_to_string('emails/invoice.html', {
        'order': order,
        'qr_code': qr_image,
        'amount': order.total_amount
    })
    
    # Send email
    email = EmailMultiAlternatives(
        subject=f'Invoice #{order.invoice_number}',
        body='Please see attached invoice',
        from_email='billing@fagierrands.com',
        to=[order.customer.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
```

**Email Template:**
```html
<!-- emails/invoice.html -->
<div style="text-align: center;">
  <h2>Invoice #{{ order.invoice_number }}</h2>
  <p>Amount Due: KES {{ amount }}</p>
  
  <div style="margin: 20px;">
    <img src="{{ qr_code }}" alt="Payment QR Code" 
         style="width: 300px; height: 300px;" />
  </div>
  
  <p>Scan with M-Pesa app to pay</p>
  <p>Or pay via Till: {{ till_number }}</p>
</div>
```

---

### Example 3: Print QR for Office

**Backend:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

def generate_qr_poster(amount, description):
    # Generate QR
    service = NCBAService()
    qr_data = service.generate_qr(
        amount=amount,
        narration=description
    )
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add text
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, 700, f"Pay KES {amount}")
    p.setFont("Helvetica", 16)
    p.drawString(100, 670, description)
    
    # Add QR code
    qr_image = ImageReader(io.BytesIO(
        base64.b64decode(qr_data['Base64QrCode'].split(',')[1])
    ))
    p.drawImage(qr_image, 150, 300, width=300, height=300)
    
    p.showPage()
    p.save()
    
    return buffer.getvalue()

# Usage
pdf = generate_qr_poster(500, "Consultation Fee")
# Print or save PDF
```

---

## Testing QR Code Generation

### Test 1: Generate QR via API
```bash
curl -X POST https://fagierrandsbackup.fagierrands.com/api/orders/payments/ncba/qr-generate/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 10,
    "order_id": 123
  }'
```

### Test 2: Generate QR in Django Shell
```python
python manage.py shell

from orders.ncba_service import NCBAService

service = NCBAService()
qr_data = service.generate_qr(
    amount=10,
    narration="Test Payment"
)

print(qr_data['StatusCode'])  # Should be "0"
print(qr_data['Base64QrCode'][:50])  # Should start with "data:image/png;base64,"

# Save to file for testing
import base64
qr_image = qr_data['Base64QrCode'].split(',')[1]
with open('test_qr.png', 'wb') as f:
    f.write(base64.b64decode(qr_image))

# Now scan test_qr.png with M-Pesa app!
```

---

## Recommended Use Cases for Your Business

### 1. **Primary: STK Push** (Online orders)
- Fast checkout
- Automatic prompt
- Best for mobile users

### 2. **Secondary: QR Code** (Flexibility)
- Invoice payments
- In-person payments
- Users without phone number
- Printed materials

### 3. **Hybrid Approach** (Best UX)
```
Checkout Page:
├─ Default: STK Push (phone number)
├─ Alternative: QR Code (scan)
└─ Fallback: Manual Till payment
```

---

## Summary

### What QR Codes Give You:
✅ Alternative payment method  
✅ No phone number needed  
✅ Reusable for fixed amounts  
✅ Professional invoicing  
✅ In-person payments  
✅ Printed marketing materials  

### Already Implemented:
✅ Backend service (`generate_qr()`)  
✅ API endpoint (`/qr-generate/`)  
✅ Narration support (order tracking)  
✅ Dynamic/fixed amounts  

### What You Need:
1. Add NCBA credentials to cPanel (same as STK)
2. Add QR option to frontend checkout
3. Test with small amount (KES 1)
4. Decide which use cases fit your business

---

**Recommendation:** Implement QR as a secondary option alongside STK Push for maximum flexibility.
